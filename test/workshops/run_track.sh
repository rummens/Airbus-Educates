#!/usr/bin/env bash
# Run the CRC smoke tests for a whole track/module in one go.
#
#   ./run_track.sh workshops-monorepo/tracks/core-track      # a track folder
#   ./run_track.sh workshops-monorepo/tracks/core-track/lab-a04-expose-app   # a single lab
#   ./run_track.sh <folder> [<folder> ...]                   # several
#
# Points at a folder, discovers every workshop under it (a dir with
# resources/workshop.yaml), and runs smoke_test.py for each — one at a time
# (CRC is small; parallel runs starve the node). It also handles the ArgoCD
# pause the portal-less deploy needs, and ALWAYS restores it on exit (even on
# Ctrl-C or error).
#
# Env overrides:
#   CTX=crc-admin                                   oc context
#   ARGO_APP=dcs-academy-tracks-and-workshops       ArgoCD app managing the Workshop CRs
#   ARGO_NS=openshift-gitops                        its namespace
#   SMOKE_ARGS="--no-links"                          extra args passed to smoke_test.py
# Flags:
#   --dry-run    show what would run (resolve labs + actions), touch nothing
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
CTX="${CTX:-crc-admin}"
ARGO_APP="${ARGO_APP:-dcs-academy-tracks-and-workshops}"
ARGO_NS="${ARGO_NS:-openshift-gitops}"
SMOKE_ARGS="${SMOKE_ARGS:---no-links}"
GREEN=$'\033[32m'; RED=$'\033[31m'; DIM=$'\033[2m'; RST=$'\033[0m'

DRY=0; folders=()
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    -h|--help) sed -n '2,25p' "$0"; exit 0 ;;
    *) folders+=("$a") ;;
  esac
done
[ ${#folders[@]} -gt 0 ] || { echo "usage: $0 [--dry-run] <folder> [<folder> ...]" >&2; exit 2; }

REPO_ROOT="$(git -C "$HERE" rev-parse --show-toplevel 2>/dev/null || echo "$HERE/../..")"

# --- discover workshops (dirs with resources/workshop.yaml) under each folder ---
is_ws() { [ -f "$1/resources/workshop.yaml" ]; }
resolve_dir() { [ -d "$1" ] && echo "$1" || { [ -d "$REPO_ROOT/$1" ] && echo "$REPO_ROOT/$1"; }; }

labs=()
for f in "${folders[@]}"; do
  dir="$(resolve_dir "$f")"
  [ -n "$dir" ] || { echo "${RED}not a folder: $f${RST}" >&2; continue; }
  if is_ws "$dir"; then
    labs+=("$(basename "$dir")")                 # pointed straight at one workshop
  else
    for d in "$dir"/*/; do is_ws "${d%/}" && labs+=("$(basename "${d%/}")"); done
  fi
done
[ ${#labs[@]} -gt 0 ] || { echo "${RED}no workshops found under: ${folders[*]}${RST}" >&2; exit 2; }

# split into runnable (has a smoke-plan with steps) vs skipped
run=(); skip=()
for name in "${labs[@]}"; do
  plan="$HERE/smoke-plans/$name.json"
  if [ ! -f "$plan" ]; then skip+=("$name  (no smoke-plan)"); continue; fi
  steps="$(python3 -c "import json;print(len(json.load(open('$plan')).get('steps',[])))" 2>/dev/null || echo 0)"
  if [ "$steps" = "0" ]; then skip+=("$name  (plan has no checks)"); else run+=("$name"); fi
done

echo "context : $CTX"
echo "argo app: $ARGO_APP (ns $ARGO_NS)"
echo "to run  : ${run[*]:-<none>}"
[ ${#skip[@]} -gt 0 ] && printf 'skipping: %s\n' "${skip[@]}"
if [ "$DRY" = 1 ]; then echo "${DIM}(dry-run — nothing executed)${RST}"; exit 0; fi
[ ${#run[@]} -gt 0 ] || { echo "nothing to run."; exit 0; }

# --- ArgoCD pause with guaranteed restore ---
PREV_AUTO="$(oc --context "$CTX" -n "$ARGO_NS" get application "$ARGO_APP" \
             -o jsonpath='{.spec.syncPolicy.automated}' 2>/dev/null)"
restore_argo() {
  [ -n "$PREV_AUTO" ] || return 0
  echo; echo ">> restoring ArgoCD auto-sync on $ARGO_APP"
  oc --context "$CTX" -n "$ARGO_NS" patch application "$ARGO_APP" --type=merge \
     -p '{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}' >/dev/null 2>&1
}
if [ -n "$PREV_AUTO" ]; then
  echo ">> pausing ArgoCD auto-sync on $ARGO_APP"
  oc --context "$CTX" -n "$ARGO_NS" patch application "$ARGO_APP" --type=merge \
     -p '{"spec":{"syncPolicy":{"automated":null}}}' >/dev/null 2>&1
  trap restore_argo EXIT INT TERM
else
  echo ">> ArgoCD auto-sync already off (leaving as-is)"
fi

# --- run each lab sequentially, collect results ---
results=(); fails=0
for name in "${run[@]}"; do
  echo; echo "================ $name ================"
  tmp="$(mktemp)"
  "$HERE/smoke_test.py" "$name" --context "$CTX" $SMOKE_ARGS 2>&1 | tee "$tmp"
  rc="${PIPESTATUS[0]}"
  summ="$(grep -oE '[0-9]+ passed, [0-9]+ failed[^;]*' "$tmp" | tail -1)"
  if grep -q 'deploy failed' "$tmp"; then
    results+=("${RED}FAIL${RST}  $name  (deploy failed)"); fails=$((fails+1))
  elif [ "$rc" -eq 0 ]; then
    results+=("${GREEN}OK  ${RST}  $name  (${summ:-ok})")
  else
    results+=("${RED}FAIL${RST}  $name  (${summ:-see log})"); fails=$((fails+1))
  fi
  rm -f "$tmp"
done

echo; echo "==================== SUMMARY ===================="
printf '%s\n' "${results[@]}"
[ ${#skip[@]} -gt 0 ] && printf '%bSKIP%b  %s\n' "$DIM" "$RST" "${skip[@]}"
echo "-------------------------------------------------"
echo "$(( ${#run[@]} - fails ))/${#run[@]} labs green"
exit "$fails"
