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
#   LOG_DIR=<path>                                   where per-lab logs go (default ./.logs/<ts>)
# Flags:
#   --dry-run    show what would run (resolve labs + actions), touch nothing
#   --no-argo    don't pause/restore ArgoCD (use if you manage sync yourself)
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
CTX="${CTX:-crc-admin}"
ARGO_APP="${ARGO_APP:-dcs-academy-tracks-and-workshops}"
ARGO_NS="${ARGO_NS:-openshift-gitops}"
SMOKE_ARGS="${SMOKE_ARGS:---no-links}"
GREEN=$'\033[32m'; RED=$'\033[31m'; DIM=$'\033[2m'; RST=$'\033[0m'

DRY=0; NO_ARGO=0; folders=()
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --no-argo) NO_ARGO=1 ;;
    -h|--help) sed -n '2,27p' "$0"; exit 0 ;;
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

LOGDIR="${LOG_DIR:-$HERE/.logs/$(date +%Y%m%d-%H%M%S)}"
echo "context : $CTX"
echo "argo app: $ARGO_APP (ns $ARGO_NS)"
echo "logs    : $LOGDIR/<lab>.log  (full per-lab output, kept)"
echo "to run  : ${run[*]:-<none>}"
[ ${#skip[@]} -gt 0 ] && printf 'skipping: %s\n' "${skip[@]}"
if [ "$DRY" = 1 ]; then echo "${DIM}(dry-run — nothing executed)${RST}"; exit 0; fi
[ ${#run[@]} -gt 0 ] || { echo "nothing to run."; exit 0; }
mkdir -p "$LOGDIR"

# --- ArgoCD pause with guaranteed restore ---
# selfHeal would revert the Workshop CRs that the portal-less deploy rewrites, so we
# pause auto-sync for the run. We ALWAYS re-enable it on exit (prune+selfHeal is the
# GitOps steady state for this cluster) — this also self-heals a prior run that was
# killed before its restore could fire. Pass --no-argo to leave ArgoCD untouched.
restore_argo() {
  echo; echo ">> restoring ArgoCD auto-sync (prune+selfHeal) on $ARGO_APP"
  oc --context "$CTX" -n "$ARGO_NS" patch application "$ARGO_APP" --type=merge \
     -p '{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}' >/dev/null 2>&1 \
     || echo "   ${RED}!! could not re-enable auto-sync — do it manually${RST}"
}
if [ "$NO_ARGO" = 1 ]; then
  echo ">> --no-argo: leaving ArgoCD sync policy untouched"
else
  echo ">> pausing ArgoCD auto-sync on $ARGO_APP for the run"
  oc --context "$CTX" -n "$ARGO_NS" patch application "$ARGO_APP" --type=merge \
     -p '{"spec":{"syncPolicy":{"automated":null}}}' >/dev/null 2>&1 \
     || echo "   ${DIM}(could not pause — continuing; selfHeal may fight the deploy)${RST}"
  trap restore_argo EXIT INT TERM
fi

# --- run each lab sequentially, collect results ---
total=${#run[@]}; k=0; results=(); fails=0
for name in "${run[@]}"; do
  k=$((k+1)); SECONDS=0
  echo
  echo "================ [$k/$total] $name ================"
  echo "${DIM}$(date '+%H:%M:%S') starting…  (log: $LOGDIR/$name.log)${RST}"
  log="$LOGDIR/$name.log"
  "$HERE/smoke_test.py" "$name" --context "$CTX" $SMOKE_ARGS 2>&1 | tee "$log"
  rc="${PIPESTATUS[0]}"
  summ="$(grep -oE '[0-9]+ passed, [0-9]+ failed[^;]*' "$log" | tail -1)"
  el="${SECONDS}s"
  echo "${DIM}$(date '+%H:%M:%S') $name done in ${el}  ·  log: $log${RST}"
  if grep -q 'deploy failed' "$log"; then
    results+=("${RED}FAIL${RST}  $name  (deploy failed, ${el})"); fails=$((fails+1))
  elif [ "$rc" -eq 0 ]; then
    results+=("${GREEN}OK  ${RST}  $name  (${summ:-ok}, ${el})")
  else
    results+=("${RED}FAIL${RST}  $name  (${summ:-see log}, ${el})"); fails=$((fails+1))
  fi
done

echo; echo "==================== SUMMARY ===================="
printf '%s\n' "${results[@]}"
[ ${#skip[@]} -gt 0 ] && printf '%bSKIP%b  %s\n' "$DIM" "$RST" "${skip[@]}"
echo "-------------------------------------------------"
echo "$(( ${#run[@]} - fails ))/${#run[@]} labs green"
echo "logs: $LOGDIR"
exit "$fails"
