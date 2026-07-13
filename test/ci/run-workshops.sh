#!/usr/bin/env bash
# Workshop tests. Two tiers:
#   fast (no cluster, safe to block merges): smoke-plan coverage + link check.
#   cluster (needs a live OpenShift/CRC): --smoke runs each workshop's graders end-to-end.
#
#   test/ci/run-workshops.sh                    # fast tier, all workshops
#   test/ci/run-workshops.sh --changed          # fast tier, only workshops changed vs base
#   test/ci/run-workshops.sh --smoke lab-a02-…  # + cluster smoke for named workshops
#   test/ci/run-workshops.sh --changed --smoke  # + cluster smoke for changed workshops
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
W=test/workshops

SMOKE=0; CHANGED=0; NAMES=()
for a in "$@"; do
  case "$a" in
    --smoke) SMOKE=1 ;;
    --changed) CHANGED=1 ;;
    --*) echo "unknown flag $a"; exit 2 ;;
    *) NAMES+=("$a") ;;
  esac
done

# Resolve which workshops the cluster smoke tier should cover.
if [ $CHANGED -eq 1 ] && [ ${#NAMES[@]} -eq 0 ]; then
  eval "$(python3 test/ci/changed.py)"
  # shellcheck disable=SC2206
  NAMES=($WORKSHOPS)
fi

fail=0

echo "########## coverage: smoke plans vs workshop content ##########"
python3 "$W/coverage_check.py" --all || fail=1

echo
echo "########## links: workshop descriptions ##########"
python3 "$W/link_check.py" --all || fail=1

if [ $SMOKE -eq 1 ]; then
  echo
  echo "########## cluster smoke (deploy → grade → teardown) ##########"
  if [ ${#NAMES[@]} -eq 0 ]; then
    echo "(--smoke given but no workshops selected; pass names or --changed)"
  fi
  for w in "${NAMES[@]}"; do
    echo "----- $w -----"
    python3 "$W/smoke_test.py" "$w" || fail=1
  done
fi

echo
if [ $fail -eq 0 ]; then
  echo "PASS: all selected workshop checks green."
else
  echo "FAIL. Cost of this failure:"
  echo "  - coverage gap  → a workshop command has no automated test; it can break silently."
  echo "  - broken link   → a learner clicks into a 404 / missing diagram."
  echo "  - smoke failure → the workshop does not actually work on the platform (examiner red)."
fi
exit $fail
