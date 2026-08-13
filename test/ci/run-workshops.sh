#!/usr/bin/env bash
# Workshop tests. Two tiers:
#   fast (no cluster, safe to block merges): smoke-plan coverage + link check.
#   cluster (needs a live OpenShift): --smoke runs each workshop's graders end-to-end.
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

# --- oc login helper ---
# Configure an active `oc` session to the dev OpenShift cluster. Called from the smoke
# block below so every cluster-tier invocation has a known-good context. Reads the same
# CI/CD variables documented in .gitlab-ci.yml (CLUSTER LOGIN block): CI_OC_HOST,
# CI_OC_TOKEN, CI_OC_USERNAME, CA_BUNDLE (or CI_OC_CA_BUNDLE), CI_OC_CONTEXT.
configure_oc() {
  if ! command -v oc >/dev/null 2>&1; then
    echo "ERROR: oc CLI not found in image — rebuild images/dcs-ci (images/build.sh)."
    return 1
  fi
  [ -n "${CI_OC_HOST:-}" ] || { echo "ERROR: CI_OC_HOST unset."; return 1; }
  [ -n "${CI_OC_TOKEN:-}" ] || { echo "ERROR: CI_OC_TOKEN unset."; return 1; }
  if oc whoami >/dev/null 2>&1; then
    echo "[oc] already logged in as $(oc whoami) to ${CI_OC_HOST}."
    return 0
  fi
  echo "[oc] logging into ${CI_OC_HOST}..."
  OC_LOGIN_ARGS=(login "${CI_OC_HOST}" --token="${CI_OC_TOKEN}")
  [ -n "${CA_BUNDLE:-}" ] && OC_LOGIN_ARGS+=(--certificate-authority="$CA_BUNDLE")
  [ -n "${CI_OC_CA_BUNDLE:-}" ] && OC_LOGIN_ARGS+=(--certificate-authority="$CI_OC_CA_BUNDLE")
  [ -n "${CI_OC_CONTEXT:-}" ] && OC_LOGIN_ARGS+=(--context="${CI_OC_CONTEXT}")
  [ -n "${CI_OC_USERNAME:-}" ] && OC_LOGIN_ARGS+=(--username="${CI_OC_USERNAME}")
  if ! oc "${OC_LOGIN_ARGS[@]}"; then
    echo "[oc] ERROR: login to ${CI_OC_HOST} failed — check CI_OC_TOKEN."
    return 1
  fi
  echo "[oc] logged in as $(oc whoami)."
  return 0
}

# A bad content sync once committed 492 zero-byte files — the labs deployed empty and no
# check noticed, because an empty file has no commands to cover and no links to break.
echo "########## sanity: no empty content files ##########"
EMPTY=$(git ls-files 'workshops-monorepo/tracks/**' | while IFS= read -r f; do [ -s "$f" ] || printf '%s\n' "$f"; done)
if [ -n "$EMPTY" ]; then
  echo "FAIL: zero-byte tracked files under workshops-monorepo/tracks:"
  echo "$EMPTY"
  fail=1
else
  echo "OK: no zero-byte files under workshops-monorepo/tracks."
fi

echo
echo "########## coverage: smoke plans vs workshop content ##########"
python3 "$W/coverage_check.py" --all || fail=1

echo
echo "########## links: content + slides + exercises + console labs ##########"
# The committed dcs_docs_base_url is a placeholder, so DCS doc links can't be fetched from
# a runner that can't reach the docs. Two separate switches, because "is the value real"
# and "can this runner fetch it" are different questions:
#   DCS_DOCS_BASE_URL       the real docs host. Without it the check FAILS (a placeholder
#                           means every DCS doc link ships as a 404 — that is a defect, not
#                           a skip, and silence here is how it reached learners).
#   DCS_DOCS_CHECK_INTERNAL true only on a runner that can actually reach that host; then
#                           the links are fetched as well, not just accepted as real.
LINK_ARGS=(--all)
# Air-gapped runner: no route to docs.openshift.com / kubernetes.io. Fetching them would
# fail every public link for a network reason, which says nothing about the content — so
# count and list them instead. Everything else (relative targets, the docs-URL guard) runs.
case "${LINK_CHECK_SKIP_EXTERNAL:-}" in 1|true|yes) LINK_ARGS+=(--skip-external) ;; esac
# Always fetch internal docs links — values.yaml shared params supply the real host, so
# the only thing that can go wrong is a placeholder value. --param lets CI override the
# host; --check-internal is on by default, toggle off with DCS_DOCS_CHECK_INTERNAL=0.
# --require-real-docs-url is always on as a safety net: if the effective docs URL is
# still a placeholder, every {{< param dcs_docs_base_url >}} link ships as a 404.
# LINK_CHECK_DEBUG=1 prints every link with its classification and whether it was fetched.
CHECK_INTERNAL="${DCS_DOCS_CHECK_INTERNAL:-1}"
[ -n "${DCS_DOCS_BASE_URL:-}" ] && LINK_ARGS+=(--param "dcs_docs_base_url=$DCS_DOCS_BASE_URL")
LINK_ARGS+=(--require-real-docs-url)
case "$CHECK_INTERNAL" in 1|true|yes) LINK_ARGS+=(--check-internal) ;; esac
[ "${LINK_CHECK_DEBUG:-}" = 1 ] && LINK_ARGS+=(--debug)
# The fix list is re-printed at the very END of the job (see below): the label check and,
# on the cluster tier, the smoke runs push it out of view, and the last screen of the log is
# the one anybody actually reads. Kept as a file so CI can also publish it as an artifact.
LINK_FIXLIST="${LINK_FIXLIST:-link-failures.txt}"
rm -f "$LINK_FIXLIST"
LINK_ARGS+=(--summary-file "$LINK_FIXLIST")
# CSV twin of the fix list — same info plus the HTTP status code, for spreadsheet analysis.
LINK_CSV="${LINK_CSV:-link-failures.csv}"
rm -f "$LINK_CSV"
LINK_ARGS+=(--summary-csv "$LINK_CSV")
python3 "$W/link_check.py" "${LINK_ARGS[@]}" || fail=1

echo
echo "########## lifecycle labels: dev/prod matches Route usage ##########"
python3 "$W/label_check.py" --all || fail=1

if [ $SMOKE -eq 1 ]; then
  echo
  echo "########## cluster smoke (deploy → grade → teardown) ##########"
  # Ensure we have an active `oc` session before deploying anything to the cluster.
  configure_oc || { echo "cluster smoke aborted: oc not configured"; exit 1; }
  if [ ${#NAMES[@]} -eq 0 ]; then
    echo "(--smoke given but no workshops selected; pass names or --changed)"
  fi
  # MR mode: SMOKE_THROWAWAY=1 deploys a throwaway Workshop hidden from the portal,
  # pulling content from SMOKE_REF (the MR branch). Default (SMOKE_REF unset) reuses
  # the configured gitRef / the catalog Workshop, as before.
  SMOKE_ARGS=(--no-links)
  if [ "${SMOKE_REF:-}" ]; then
    SMOKE_ARGS+=(--ref "$SMOKE_REF")
  fi
  if [ "${SMOKE_THROWAWAY:-}" = "1" ]; then
    SMOKE_ARGS+=(--throwaway)
  fi
  for w in "${NAMES[@]}"; do
    echo "----- $w -----"
    python3 "$W/smoke_test.py" "$w" "${SMOKE_ARGS[@]}" || fail=1
  done
fi

echo
if [ $fail -eq 0 ]; then
  echo "PASS: all selected workshop checks green."
else
  echo "FAIL. Cost of this failure:"
  echo "  - coverage gap  → a workshop command has no automated test; it can break silently."
  echo "  - broken link   → a learner clicks into a 404 / missing diagram."
  echo "  - label problem → a lab's dev/prod lifecycle label doesn't match its Route usage."
  echo "  - smoke failure → the workshop does not actually work on the platform (examiner red)."
fi

# LAST thing in the log, always, whichever check failed: the copy-paste fix list.
# lab · file:line · reason · url — open that file at that line and fix that link.
if [ -s "$LINK_FIXLIST" ]; then
  echo
  echo "################ LINKS TO FIX ($(wc -l < "$LINK_FIXLIST" | tr -d ' ')) ################"
  echo "lab                              file:line                                   reason  url"
  cat "$LINK_FIXLIST"
  echo "################ end links to fix ################"
fi
exit $fail
