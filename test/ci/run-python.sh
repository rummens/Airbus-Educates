#!/usr/bin/env bash
# Portal unit tests + coverage gate. No cluster needed. Fast lane — safe to block merges on.
#   test/ci/run-python.sh
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

MIN=${COVERAGE_MIN:-90}
echo "=== portal unit tests (pytest, coverage gate ${MIN}%) ==="

python3 -m pytest test/portal/test_portal.py \
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
