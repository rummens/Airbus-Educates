#!/usr/bin/env bash
#
# Relocate the Educates installer imgpkg bundle into a private registry (Harbor)
# for an air-gapped install.
#
# WHY THIS EXISTS (read OFFLINE-MIRROR-IMAGES.md too):
#   The installer bundle carries an internal ImagesLock (.imgpkg/images.yml) that
#   pins every platform image by ghcr.io DIGEST. Harbor "replication" copies image
#   tags but does NOT rewrite that lock or write the ImageLocations metadata kbld
#   needs — so kbld/kapp still try to pull the inner images from ghcr.io and the
#   air-gapped install fails. `imgpkg copy` is the ONLY thing that relocates a
#   bundle correctly (copies all referenced images + writes the location metadata).
#   Plain (non-bundle) images — kapp-controller, oauth-proxy, kube-state-metrics,
#   workshop content — can stay on Harbor replication; only the BUNDLE needs this.
#
# MODES:
#   direct  — one host can reach BOTH ghcr.io and your registry (simplest).
#   export  — internet-connected host: bundle + all images -> a single .tar.
#   import  — air-gapped host (can reach your registry): .tar -> your registry.
#             (export on one side, carry the tar across the gap, import on the other.)
#
# USAGE:
#   DEST_REGISTRY=harbor.example.dcs ./mirror-educates-bundle.sh direct
#   DEST_REGISTRY=harbor.example.dcs ./mirror-educates-bundle.sh export   # internet side
#   DEST_REGISTRY=harbor.example.dcs ./mirror-educates-bundle.sh import   # air-gapped side
#
# PREREQS:
#   * imgpkg (Carvel):  https://carvel.dev/imgpkg/  (or: brew install vmware-tanzu/carvel/imgpkg)
#   * Registry auth. Log in first so imgpkg can push/pull:
#       docker login harbor.example.dcs        # (or: podman login / imgpkg --registry-* flags)
#     ghcr.io/educates/* is public — no login needed for the source.
#
# AFTER MIRRORING:
#   Set the destination as the chart's registry host so the install uses your copy:
#     dcs-academy-platform values:  global.registry.host: "harbor.example.dcs"
#   The chart keeps the bundle path and only swaps the host, i.e. it will pull
#     harbor.example.dcs/educates/educates-installer:<version>
#   So DEST_REPO below MUST be  <DEST_REGISTRY>/educates/educates-installer.

set -euo pipefail

VERSION="${EDUCATES_VERSION:-3.7.2}"
SRC_BUNDLE="ghcr.io/educates/educates-installer:${VERSION}"

DEST_REGISTRY="${DEST_REGISTRY:?set DEST_REGISTRY (your registry host, e.g. harbor.example.dcs) — must equal global.registry.host}"
# Keep the /educates/educates-installer path — the chart expects it under the host.
DEST_REPO="${DEST_REPO:-${DEST_REGISTRY}/educates/educates-installer}"

TAR="${TAR:-educates-installer-${VERSION}.tar}"
MODE="${1:-direct}"

log() { printf '\n\033[1m>>> %s\033[0m\n' "$*"; }
need() { command -v "$1" >/dev/null 2>&1 || { echo "ERROR: missing required tool: $1" >&2; exit 1; }; }

need imgpkg

case "$MODE" in
  direct)
    log "Relocating ${SRC_BUNDLE} -> ${DEST_REPO} (direct registry-to-registry)"
    imgpkg copy -b "${SRC_BUNDLE}" --to-repo "${DEST_REPO}"
    ;;

  export)
    log "Exporting ${SRC_BUNDLE} + all referenced images -> ${TAR}"
    imgpkg copy -b "${SRC_BUNDLE}" --to-tar "${TAR}"
    log "Done. Move ${TAR} across the air gap, then on the internal host run:"
    echo "  DEST_REGISTRY=${DEST_REGISTRY} TAR=${TAR} $0 import"
    ;;

  import)
    [ -f "${TAR}" ] || { echo "ERROR: ${TAR} not found (run 'export' first and copy it here)" >&2; exit 1; }
    log "Importing ${TAR} -> ${DEST_REPO} (relocates + writes ImageLocations)"
    imgpkg copy --tar "${TAR}" --to-repo "${DEST_REPO}"
    ;;

  *)
    echo "usage: DEST_REGISTRY=<host> $0 [direct|export|import]" >&2
    exit 1
    ;;
esac

# Verify (skip after export — nothing is in the registry yet).
if [ "${MODE}" != "export" ]; then
  log "Verifying the relocated bundle is pullable from ${DEST_REPO}:${VERSION}"
  tmp="$(mktemp -d)"
  if imgpkg pull -b "${DEST_REPO}:${VERSION}" -o "${tmp}" >/dev/null 2>&1; then
    echo "OK: bundle pulled from ${DEST_REPO}:${VERSION}"
    if [ -f "${tmp}/.imgpkg/images.yml" ]; then
      echo "Referenced images in the relocated lock:"
      grep -E 'image:' "${tmp}/.imgpkg/images.yml" | sed 's/^/  /' || true
    fi
  else
    echo "WARN: could not pull ${DEST_REPO}:${VERSION} back — check registry auth / repo path" >&2
  fi
  rm -rf "${tmp}"
  log "Next: set global.registry.host=${DEST_REGISTRY} on dcs-academy-platform (and dcs-academy-portal / workshops), and mirror the non-bundle images per OFFLINE-MIRROR-IMAGES.md."
fi
