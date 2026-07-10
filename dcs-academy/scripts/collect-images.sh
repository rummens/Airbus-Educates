#!/usr/bin/env bash
# collect-images.sh — emit the deduplicated container-image manifest across all
# academy workshops, for Harbor mirroring. DCS is air-gapped: every image must
# resolve to Harbor. References to external registries are a house-standard
# violation and are reported as errors (non-zero exit), not mirrored silently.
#
# Usage:
#   ./scripts/collect-images.sh            # scan ../workshops, print manifest
#   ./scripts/collect-images.sh <dir>      # scan <dir> instead
#   ./scripts/collect-images.sh --selftest # run the built-in self-test
#
# See the authoring skill's image-manifest-reference.md.
set -euo pipefail

EXTERNAL_RE='(^|/)(docker\.io|index\.docker\.io|quay\.io|ghcr\.io|registry\.k8s\.io|k8s\.gcr\.io|gcr\.io|public\.ecr\.aws|mcr\.microsoft\.com)/'

collect() {
  local workshops="$1"
  [ -d "$workshops" ] || { echo "no workshops dir: $workshops" >&2; return 1; }

  local all="" wdir cfg reg
  for wdir in "$workshops"/*/; do
    [ -d "$wdir" ] || continue
    reg=""
    cfg="$wdir/workshop/config.yaml"
    if [ -f "$cfg" ]; then
      reg="$(sed -nE 's/^[[:space:]]*dcs_registry:[[:space:]]*["'\'']?([^"'\''[:space:]]+).*/\1/p' "$cfg" | head -1)"
    fi
    # every `image: <value>` with a non-empty value (mapping-only `image:` lines
    # are skipped). Values may contain spaces (Hugo shortcodes), so capture to
    # end of line and trim quotes/comments rather than grabbing a single token.
    while IFS= read -r img; do
      [ -z "$img" ] && continue
      [ -n "$reg" ] && img="${img//\{\{< param dcs_registry >\}\}/$reg}"
      all+="$img"$'\n'
    done < <(grep -rhE '(^|[[:space:]]|-)image:[[:space:]]+[^[:space:]]' "$wdir" 2>/dev/null \
               | sed -E 's/.*image:[[:space:]]*//; s/[[:space:]]*#.*$//; s/^["'\'']//; s/["'\''][[:space:]]*$//; s/[[:space:]]*$//')
  done

  local manifest external unresolved
  manifest="$(printf '%s' "$all" | sed '/^$/d' | sort -u)"
  [ -z "$manifest" ] && { echo "no image references found" >&2; return 0; }

  printf '%s\n' "$manifest"

  # Classify each image. Compliant = resolved to a fully-qualified Harbor-style
  # registry host (first path segment contains a '.' or ':'). Anything else is a
  # violation: an explicit external registry, or a bare/Docker-Hub image with no
  # registry host (e.g. nginx:latest). Unresolved variables are warned, not failed.
  local violations="" unresolved="" img first
  while IFS= read -r img; do
    [ -z "$img" ] && continue
    case "$img" in *'{{<'*|*'$(image_repository)'*) unresolved+="$img"$'\n'; continue;; esac
    first="${img%%/*}"
    if [ "$first" = "$img" ]; then violations+="$img"$'\n'; continue; fi
    case "$first" in *.*|*:*) : ;; *) violations+="$img"$'\n'; continue;; esac
    printf '%s' "$img" | grep -qE "$EXTERNAL_RE" && violations+="$img"$'\n'
  done <<< "$manifest"

  [ -n "$unresolved" ] && printf 'WARN: unresolved variables (resolve at publish time):\n%s' "$unresolved" >&2
  if [ -n "$violations" ]; then
    printf 'ERROR: non-Harbor / external images (house-standard violation — fix the workshop):\n%s' "$violations" >&2
    return 2
  fi
  return 0
}

selftest() {
  local t; t="$(mktemp -d)"
  mkdir -p "$t/workshops/lab-x/workshop" "$t/workshops/lab-x/exercises"
  printf 'params:\n  dcs_registry: "harbor.test/dcs"\n' > "$t/workshops/lab-x/workshop/config.yaml"
  printf 'spec:\n  x:\n    image: "{{< param dcs_registry >}}/app:1.0"\n' > "$t/workshops/lab-x/resources.yaml"
  printf 'containers:\n- image: nginx:latest\n' > "$t/workshops/lab-x/exercises/bad.yaml"

  local out rc=0
  out="$(collect "$t/workshops" 2>/dev/null)" || true
  collect "$t/workshops" >/dev/null 2>&1 || rc=$?

  local fail=0
  echo "$out" | grep -qx "harbor.test/dcs/app:1.0" || { echo "FAIL: param not resolved to Harbor"; fail=1; }
  [ "$rc" -eq 2 ] || { echo "FAIL: external registry (nginx:latest) not flagged (rc=$rc)"; fail=1; }
  rm -rf "$t"
  if [ "$fail" -eq 0 ]; then echo "selftest OK"; else echo "selftest FAILED"; return 1; fi
}

main() {
  case "${1:-}" in
    --selftest) selftest ;;
    "") collect "$(cd "$(dirname "$0")/.." && pwd)/workshops" ;;
    *) collect "$1" ;;
  esac
}
main "$@"
