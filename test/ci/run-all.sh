#!/usr/bin/env bash
# Local dev runner — mirrors the GitLab CI fast tier end-to-end:
#   1. portal-tests      (pytest + coverage gate)
#   2. workshop-static   (coverage + links + labels)
#
# Env vars mirror .gitlab-ci.yml. All are optional with sane defaults:
#   CI_BASE_IMAGE             ghcr.io/rummens/dcs-ci:dev
#   COVERAGE_MIN              90
#   DCS_DOCS_BASE_URL         real internal docs host (enables --param + --check-internal)
#   DCS_DOCS_CHECK_INTERNAL   1|true|yes to fetch internal links; default 1 when docs url set
#   LINK_CHECK_SKIP_EXTERNAL  1|true|yes for air-gapped runners
#
# Override individually:
#   DCS_DOCS_BASE_URL=https://docs.internal ./run-all.sh
#   DCS_DOCS_CHECK_INTERNAL=0 LINK_CHECK_SKIP_EXTERNAL=1 ./run-all.sh
#
# Cluster smoke is NOT included — that needs a live OpenShift with oc logged in.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

COVERAGE_MIN="${COVERAGE_MIN:-90}"
DCS_DOCS_CHECK_INTERNAL="${DCS_DOCS_CHECK_INTERNAL:-}"

# Default --check-internal ON when a docs base URL is provided, so local runs get the
# same fidelity as CI would with DCS_DOCS_CHECK_INTERNAL set.
if [ -n "${DCS_DOCS_BASE_URL:-}" ] && [ -z "${DCS_DOCS_CHECK_INTERNAL:-}" ]; then
  DCS_DOCS_CHECK_INTERNAL=1
  export DCS_DOCS_CHECK_INTERNAL
fi

fail=0

echo "########## 1. portal unit tests + coverage gate (${COVERAGE_MIN}%) ##########"
bash test/ci/run-python.sh || fail=1

echo
echo "########## 2. workshop checks (coverage + links + labels) ##########"
if [ -n "${DCS_DOCS_BASE_URL:-}" ]; then
  echo "    DCS_DOCS_BASE_URL=${DCS_DOCS_BASE_URL}"
else
  echo "    DCS_DOCS_BASE_URL= (unset — link check will fail on placeholder docs URL)"
fi
if [ -n "${DCS_DOCS_CHECK_INTERNAL:-}" ]; then
  echo "    DCS_DOCS_CHECK_INTERNAL=${DCS_DOCS_CHECK_INTERNAL}"
fi
if [ -n "${LINK_CHECK_SKIP_EXTERNAL:-}" ]; then
  echo "    LINK_CHECK_SKIP_EXTERNAL=${LINK_CHECK_SKIP_EXTERNAL}"
fi
bash test/ci/run-workshops.sh || fail=1

echo
if [ $fail -eq 0 ]; then
  echo "ALL FAST-TIER CHECKS PASSED."
else
  echo "SOME CHECKS FAILED."
  echo "Fast tier: portal-tests + workshop-static (coverage, links, labels)."
  echo "Cluster smoke (--smoke) requires a live OpenShift with oc logged in."
fi

echo
echo "########## proxy environment (export in shell before running to unblock curl-based link fetches) ##########"
echo "export HTTP_PROXY=\"http://divproxy01.dsmain.ds.corp:8080\""
echo "export HTTPS_PROXY=\"http://divproxy01.dsmain.ds.corp:8080\""
echo "export http_proxy=\"http://divproxy01.dsmain.ds.corp:8080\""
echo "export https_proxy=\"http://divproxy01.dsmain.ds.corp:8080\""
echo "export NO_PROXY=\"localhost,127.0.0.1,.airbusds.corp,.aircloud.common.airbusds.corp,.dcs.common.airbusds.corp,.dsmain.ds.corp\""
echo "##########################################################################"
exit $fail
