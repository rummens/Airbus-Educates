#!/bin/sh
# Relocate the Educates installer imgpkg bundle into a private registry.
#
# imgpkg copy pulls the bundle + EVERY image its ImagesLock references and pushes
# them into DEST_REPO, writing the ImageLocations metadata kbld/kapp need — the
# part plain registry replication cannot do. It is IDEMPOTENT: blobs already in the
# destination are skipped, so re-running (PreSync/PostSync each ArgoCD sync) is a
# cheap no-op once the bundle is in place.
#
# Env (set by the Job):
#   SRC_BUNDLE  upstream bundle ref, e.g. ghcr.io/educates/educates-installer:3.7.2
#   DEST_REPO   target repo (no tag), e.g. registry.example/dcs/educates/educates-installer
#   IMGPKG_REGISTRY_HOSTNAME_0/_USERNAME_0/_PASSWORD_0  push creds for the dest host
#   HTTP(S)_PROXY / NO_PROXY  egress proxy to reach the source registry (ghcr)
set -eu

: "${SRC_BUNDLE:?set SRC_BUNDLE (e.g. ghcr.io/educates/educates-installer:3.7.2)}"
: "${DEST_REPO:?set DEST_REPO (e.g. myregistry/dcs/educates/educates-installer)}"

# DEBUG=1 turns on imgpkg's --debug output and shell tracing (verbose registry/HTTP
# logging). Set via bundleMirror.debug in the chart.
DBG=""
case "${DEBUG:-}" in
  1|true|TRUE|yes|on) DBG="--debug"; echo ">>> DEBUG on (imgpkg --debug + shell trace)"; set -x ;;
esac

echo ">>> relocating bundle"
echo "    from: ${SRC_BUNDLE}"
echo "    to:   ${DEST_REPO}"
[ -n "${HTTPS_PROXY:-${https_proxy:-}}" ] && echo "    via proxy: ${HTTPS_PROXY:-$https_proxy}" || true

# Log the registry logins imgpkg will use (creds come from IMGPKG_REGISTRY_* env;
# imgpkg authenticates per-request, there is no separate login step). Passwords are
# never printed. Index 0 is the destination push target.
echo ">>> registry authentication:"
n=0
while [ "$n" -lt 5 ]; do
  eval "h=\${IMGPKG_REGISTRY_HOSTNAME_${n}:-}"
  eval "u=\${IMGPKG_REGISTRY_USERNAME_${n}:-}"
  if [ -n "${h}" ]; then
    role="source"
    [ "$n" = "0" ] && role="DESTINATION (push)"
    echo "    [${n}] logging in to ${h} as '${u:-<anonymous>}' — ${role}"
  fi
  n=$((n + 1))
done
[ -z "${IMGPKG_REGISTRY_HOSTNAME_0:-}" ] && echo "    (no destination creds set — pushing anonymously)" || true

imgpkg copy -b "${SRC_BUNDLE}" --to-repo "${DEST_REPO}" ${DBG} ${IMGPKG_EXTRA_ARGS:-}

echo ">>> relocated OK. Tags now present in ${DEST_REPO}:"
imgpkg tag list -i "${DEST_REPO}" 2>/dev/null | sed 's/^/    /' || true
echo ">>> done"
