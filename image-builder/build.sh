#!/usr/bin/env bash
# Monorepo image builder: detect changed top-level folders, create/update an
# OpenShift BuildConfig per (folder, branch), trigger the build, push to an
# external registry. Cleanup reconciles orphaned BCs + registry tags.
#
# Subcommands:
#   build            build every changed+eligible folder for the current branch
#   cleanup          delete BCs (and their registry tags) whose branch no longer
#                    exists on the remote  (source-branch-deleted reconcile)
#   cleanup <branch> delete BCs/tags for one specific (sanitized) branch
#   selftest         run pure-logic asserts, no cluster needed
#
# A folder is "eligible" if it holds a Dockerfile, Containerfile, or build_config.json.
set -euo pipefail

# ---- config (all overridable via env / GitLab CI variables) ----------------
BUILD_NAMESPACE="${BUILD_NAMESPACE:-image-builds}"
REGISTRY_BASE="${REGISTRY_BASE:-}"            # <host>/<project>, required for build
PUSH_SECRET="${PUSH_SECRET:-image-push}"      # docker-registry secret for output
GIT_SECRET="${GIT_SECRET:-git-source}"        # basic-auth secret for source clone
SOURCE_GIT_URI="${SOURCE_GIT_URI:-${CI_PROJECT_URL:-}.git}"
DEFAULT_BRANCH="${DEFAULT_BRANCH:-${CI_DEFAULT_BRANCH:-main}}"
BUILD_ALL="${BUILD_ALL:-false}"               # true = ignore change detection

LABEL_BRANCH="dcs.build/branch"
LABEL_FOLDER="dcs.build/folder"

log() { printf '\033[1;34m==>\033[0m %s\n' "$*" >&2; }
die() { printf '\033[1;31mERR\033[0m %s\n' "$*" >&2; exit 1; }

# ---- pure helpers (covered by selftest) ------------------------------------

# RFC1123-ish label/name: lowercase, non-alnum -> '-', squeeze, trim, <=63.
sanitize() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/-+/-/g; s/^-//; s/-$//' \
    | cut -c1-63 | sed -E 's/-$//'
}

# BC name from folder+branch. Truncate long combos; on truncation append a short
# hash of the full key so distinct branches don't collide.
# ponytail: 63-char cap can theoretically collide after hashing; add a longer
#           name scheme only if that ever bites.
bc_name() {
  local key raw
  key="$(sanitize "$1")--$(sanitize "$2")"
  raw="$key"
  if [ "${#raw}" -gt 63 ]; then
    local h; h="$(printf '%s' "$1/$2" | cksum | cut -d' ' -f1)"
    raw="$(printf '%s' "$key" | cut -c1-54)-${h}"
    raw="$(printf '%s' "$raw" | cut -c1-63)"
  fi
  printf '%s' "$raw"
}

# Top-level dir of a repo-relative path, or empty for root-level files.
top_dir() { printf '%s' "$1" | awk -F/ 'NF>1{print $1}'; }

is_eligible() {
  [ -f "$1/Dockerfile" ] || [ -f "$1/Containerfile" ] || [ -f "$1/build_config.json" ]
}

# ---- change detection ------------------------------------------------------

changed_dirs() {
  local range
  if [ "$BUILD_ALL" = "true" ]; then
    for d in */; do printf '%s\n' "${d%/}"; done; return
  fi
  if [ -n "${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-}" ]; then
    git fetch -q origin "$CI_MERGE_REQUEST_TARGET_BRANCH_NAME" || true
    range="origin/${CI_MERGE_REQUEST_TARGET_BRANCH_NAME}...HEAD"
  elif [ -n "${CI_COMMIT_BEFORE_SHA:-}" ] && \
       [ "$CI_COMMIT_BEFORE_SHA" != "0000000000000000000000000000000000000000" ]; then
    range="${CI_COMMIT_BEFORE_SHA}..${CI_COMMIT_SHA:-HEAD}"
  else
    # first push of a new branch (no before-sha): diff vs default branch
    git fetch -q origin "$DEFAULT_BRANCH" || true
    range="origin/${DEFAULT_BRANCH}...HEAD"
  fi
  git diff --name-only "$range" 2>/dev/null | while read -r f; do
    top_dir "$f"
  done | sort -u | sed '/^$/d'
}

# ---- secrets (idempotent create-or-update) ---------------------------------

ensure_secrets() {
  : "${REGISTRY_SERVER:?}" "${REGISTRY_USER:?}" "${REGISTRY_PASS:?}"
  oc create secret docker-registry "$PUSH_SECRET" \
    --docker-server="$REGISTRY_SERVER" \
    --docker-username="$REGISTRY_USER" \
    --docker-password="$REGISTRY_PASS" \
    -n "$BUILD_NAMESPACE" --dry-run=client -o yaml | oc apply -f -
  : "${GIT_USER:?}" "${GIT_TOKEN:?}"
  oc create secret generic "$GIT_SECRET" \
    --type=kubernetes.io/basic-auth \
    --from-literal=username="$GIT_USER" \
    --from-literal=password="$GIT_TOKEN" \
    -n "$BUILD_NAMESPACE" --dry-run=client -o yaml | oc apply -f -
}

# ---- BuildConfig assembly (jq) ---------------------------------------------

# Emit a BuildConfig JSON on stdout for one folder.
render_bc() {
  local dir="$1" branch="$2" name="$3" output="$4" contextdir="$5"
  local cfg="$dir/build_config.json"
  local s2i df env args res nocache
  s2i=""; df=""; env="null"; args="null"; res="null"; nocache="false"
  if [ -f "$cfg" ]; then
    s2i="$(jq -r '.s2iImage // empty' "$cfg")"
    df="$(jq -r '.dockerfilePath // empty' "$cfg")"
    env="$(jq -c 'if (.env // [] | length) > 0 then .env else null end' "$cfg")"
    args="$(jq -c 'if (.buildArgs // [] | length) > 0 then .buildArgs else null end' "$cfg")"
    res="$(jq -c '.resources // null' "$cfg")"
    nocache="$(jq -r '.noCache // false' "$cfg")"
  fi

  local strategy
  if [ -n "$s2i" ]; then
    strategy="$(jq -nc --arg img "$s2i" --argjson env "$env" \
      '{sourceStrategy:{from:{kind:"DockerImage",name:$img},env:$env}}')"
  else
    [ -z "$df" ] && { [ -f "$dir/Dockerfile" ] && df=Dockerfile || df=Containerfile; }
    strategy="$(jq -nc --arg df "$df" --argjson env "$env" \
      --argjson args "$args" --argjson nc "$nocache" \
      '{dockerStrategy:{dockerfilePath:$df,env:$env,buildArgs:$args,noCache:$nc}}')"
  fi

  jq -n \
    --arg name "$name" --arg ns "$BUILD_NAMESPACE" \
    --arg branch "$(sanitize "$branch")" --arg folder "$(sanitize "$dir")" \
    --arg gituri "$SOURCE_GIT_URI" --arg gitref "$branch" \
    --arg ctx "$contextdir" --arg output "$output" \
    --arg push "$PUSH_SECRET" --arg gitsec "$GIT_SECRET" \
    --arg blk "$LABEL_BRANCH" --arg flk "$LABEL_FOLDER" \
    --argjson strategy "$strategy" --argjson resources "$res" \
    '{
      apiVersion:"build.openshift.io/v1", kind:"BuildConfig",
      metadata:{name:$name, namespace:$ns,
        labels:{($blk):$branch, ($flk):$folder}},
      spec:{
        runPolicy:"Serial",
        source:{type:"Git", git:{uri:$gituri, ref:$gitref}, contextDir:$ctx,
                sourceSecret:{name:$gitsec}},
        strategy:$strategy,
        output:{to:{kind:"DockerImage", name:$output}, pushSecret:{name:$push}},
        resources:$resources
      }
    }
    | del(.. | nulls)'
}

build_one() {
  local dir="$1" branch="$2"
  local cfg="$dir/build_config.json"
  local repo tag ctx name output

  repo="$REGISTRY_BASE/$dir"
  tag="$(sanitize "$branch")"
  ctx="$dir"
  if [ -f "$cfg" ]; then
    local r t c
    r="$(jq -r '.destinationRepo // empty' "$cfg")"; [ -n "$r" ] && repo="$r"
    t="$(jq -r '.tag // empty' "$cfg")"; [ -n "$t" ] && tag="$(sanitize "$t")"
    c="$(jq -r '.contextDir // empty' "$cfg")"; [ -n "$c" ] && ctx="$dir/$c"
  fi
  output="$repo:$tag"
  name="$(bc_name "$dir" "$branch")"

  log "build_one: $dir -> $output  (bc/$name)"
  render_bc "$dir" "$branch" "$name" "$output" "$ctx" | oc apply -f -
  oc start-build "$name" -n "$BUILD_NAMESPACE" --follow
}

do_build() {
  : "${REGISTRY_BASE:?set REGISTRY_BASE, e.g. harbor.example.com/dcs}"
  ensure_secrets
  local branch="${CI_COMMIT_REF_NAME:-$(git rev-parse --abbrev-ref HEAD)}"
  local built=0
  while read -r dir; do
    [ -z "$dir" ] && continue
    [ -d "$dir" ] || continue
    is_eligible "$dir" || { log "skip $dir (no Dockerfile/Containerfile/build_config.json)"; continue; }
    build_one "$dir" "$branch"
    built=$((built+1))
  done < <(changed_dirs)
  log "built $built folder(s)"
}

# ---- cleanup ---------------------------------------------------------------

# Delete BCs matching a sanitized branch label + their registry tags.
delete_branch() {
  local b="$1"
  [ "$b" = "$(sanitize "$DEFAULT_BRANCH")" ] && { log "refuse to clean default branch"; return; }
  local imgs
  imgs="$(oc get bc -n "$BUILD_NAMESPACE" -l "$LABEL_BRANCH=$b" \
          -o jsonpath='{.items[*].spec.output.to.name}' 2>/dev/null || true)"
  for img in $imgs; do
    log "skopeo delete $img"
    skopeo delete --creds "${REGISTRY_USER}:${REGISTRY_PASS}" "docker://$img" || \
      log "  (tag already gone or delete disabled)"
  done
  oc delete bc -n "$BUILD_NAMESPACE" -l "$LABEL_BRANCH=$b" --ignore-not-found
}

do_cleanup() {
  if [ -n "${1:-}" ]; then delete_branch "$(sanitize "$1")"; return; fi
  # reconcile: any BC branch-label with no matching live remote branch -> orphan
  local live existing
  live="$(git ls-remote --heads origin | awk '{print $2}' | sed 's#refs/heads/##' \
          | while read -r b; do sanitize "$b"; done | sort -u)"
  existing="$(oc get bc -n "$BUILD_NAMESPACE" -L "$LABEL_BRANCH" \
              -o jsonpath="{range .items[*]}{.metadata.labels.$LABEL_BRANCH}{'\n'}{end}" \
              2>/dev/null | sort -u | sed '/^$/d')"
  while read -r b; do
    [ -z "$b" ] && continue
    if ! grep -qxF "$b" <<<"$live"; then
      log "orphan branch '$b' -> cleanup"
      delete_branch "$b"
    fi
  done <<<"$existing"
}

# ---- selftest --------------------------------------------------------------

selftest() {
  local f
  [ "$(sanitize 'Feature/Foo_Bar')" = "feature-foo-bar" ] || die "sanitize case/slash"
  [ "$(sanitize '--weird__name--')" = "weird-name" ] || die "sanitize trim/squeeze"
  [ "$(top_dir 'python-base/Dockerfile')" = "python-base" ] || die "top_dir nested"
  [ -z "$(top_dir 'README.md')" ] || die "top_dir root file"
  f="$(bc_name 'python-base' 'main')"; [ "$f" = "python-base--main" ] || die "bc_name simple ($f)"
  f="$(bc_name 'x' "$(printf 'b%.0s' $(seq 1 80))")"; [ "${#f}" -le 63 ] || die "bc_name len ${#f}"
  # distinct long branches must not collide after truncation
  local a bb
  a="$(bc_name 'svc' "release-2026-01-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")"
  bb="$(bc_name 'svc' "release-2026-01-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")"
  [ "$a" != "$bb" ] || die "bc_name long collision"
  echo "selftest OK"
}

# ---- dispatch --------------------------------------------------------------
cmd="${1:-build}"; shift || true
case "$cmd" in
  build)    do_build ;;
  cleanup)  do_cleanup "${1:-}" ;;
  selftest) selftest ;;
  *) die "unknown command: $cmd (build|cleanup|selftest)" ;;
esac
