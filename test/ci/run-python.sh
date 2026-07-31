#!/usr/bin/env bash
# Portal unit tests + coverage gate. No cluster needed. Fast lane — safe to block merges on.
#   test/ci/run-python.sh
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

MIN=${COVERAGE_MIN:-90}
echo "=== portal unit tests (pytest, coverage gate ${MIN}%) ==="

# The whole directory, not just test_portal.py — test_slides.py and
# test_reap_validate.py used to be collected by nobody, so their modules counted as
# uncovered and the gate failed on code that IS tested.
# -W error::ResourceWarning — a leaked DB connection / file handle is a real defect in a
# long-lived pod, and as a mere warning it was 80 lines of noise nobody read. Errors now.
python3 -m pytest test/portal -W error::ResourceWarning \
    --cov=portal --cov-report=term-missing "--cov-fail-under=${MIN}" -q
rc=$?

echo
if [ $rc -eq 0 ]; then
  echo "PASS: portal tests green and coverage >= ${MIN}%."
else
  echo "FAIL (rc=$rc). Cost of this failure:"
  echo "  - a broken portal route/DB/auth path ships to learners, OR"
  echo "  - coverage dropped below ${MIN}% — new portal code has no test."
fi
exit $rc
