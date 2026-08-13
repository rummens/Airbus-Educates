#!/usr/bin/env bash
# Local smoke runner for the dev cluster — quick way to validate a workshop end-to-end.
#
#   ./smoke.sh <lab>               # deploy, run smoke plan, tear down
#   ./smoke.sh <lab> --keep        # leave it running (inspect logs)
#   ./smoke.sh <lab> --no-links    # skip link check (faster)
#   ./smoke.sh --all               # run the whole dev track
#   ./smoke.sh --help               # show usage
#
# Env:
#   CTX              oc context, default: current context
#   SMOKE_ID         session id, default: 99 (high to avoid clashing with manual runs)
#   SMOKE_ARGS       extra args passed to smoke_test.py (e.g. --keep)
#   SMOKE_REF        git ref to test (MR mode). Unset = use configured gitRef/catalog Workshop.
#   SMOKE_THROWAWAY  1 = deploy a throwaway Workshop hidden from the portal, pulling content
#                    from SMOKE_REF; never touches the Argo-managed catalog Workshop.
#
# Usage patterns:
#   bash test/workshops/smoke.sh lab-a02-kubernetes-essentials            # catalog content
#   SMOKE_THROWAWAY=1 SMOKE_REF=feature/my-mr bash test/workshops/smoke.sh lab-a02-kubernetes-essentials
#   SMOKE_THROWAWAY=1 SMOKE_REF=feature/my-mr bash test/workshops/smoke.sh --all

set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

CTX="${CTX:-$(oc config current-context 2>/dev/null || echo logged-user)}"
SID="${SMOKE_ID:-99}"

if [ $# -eq 0 ]; then
    echo "usage: $0 <lab> [--keep|--no-links] | $0 --all"
    exit 2
fi

if [ "$1" = "--all" ]; then
    shift
    # Run the whole dev track by default. Any extra flags (e.g. --dry-run, --no-argo)
    # are passed through to run_track.sh — supply a track/folder path to override.
    bash test/workshops/run_track.sh tracks/core-track "$@"
    exit $?
fi

if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    cat <<'USAGE'
usage: smoke.sh <lab> [--keep|--no-links] | smoke.sh --all

Local smoke runner for the dev cluster — deploys a workshop, runs its smoke
plan, and tears it down.

  ./smoke.sh lab-a02-kubernetes-essentials             # catalog content
  ./smoke.sh lab-a02-kubernetes-essentials --keep      # leave it running
  ./smoke.sh --all                                     # run the whole dev track

Env overrides:
  CTX              oc context (default: current)
  SMOKE_ID         session id, default 99
  SMOKE_REF        git ref to test (MR mode)
  SMOKE_THROWAWAY  1 = deploy a throwaway Workshop hidden from the portal
  SMOKE_NO_LINKS   1 = skip external link check
USAGE
    exit 0
fi

LAB="$1"
shift

echo "========== $LAB =========="
echo "context : $CTX"
echo "session : $LAB-w$SID"
EXTRA_ARGS=()
if [ "${SMOKE_REF:-}" ]; then
    EXTRA_ARGS+=(--ref "$SMOKE_REF")
fi
if [ "${SMOKE_THROWAWAY:-}" = "1" ]; then
    EXTRA_ARGS+=(--throwaway)
fi
if [ "${SMOKE_NO_LINKS:-}" = "1" ]; then
    EXTRA_ARGS+=(--no-links)
fi
python3 test/workshops/smoke_test.py "$LAB" --context "$CTX" --id "$SID" "${EXTRA_ARGS[@]}" "$@" || {
    echo "FAILED: $LAB"
    exit 1
}
echo "PASSED: $LAB"
