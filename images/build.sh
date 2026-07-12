#!/usr/bin/env bash
# Build + push the DCS Academy images to the GitHub Container Registry.
#
#   ./build.sh                # arm64 (CRC target), the default
#   MULTIARCH=1 ./build.sh    # amd64 + arm64 via buildx (for x86 clusters too)
#
# Requires: docker logged in to ghcr.io (write:packages) and to the Red Hat
# registry (for the UBI base of hello-dcs). After first push, make the packages
# public in GitHub for unauthenticated cluster pulls.
set -euo pipefail
REG="${REG:-ghcr.io/rummens}"
cd "$(dirname "$0")"

build_push() {           # <dir> <image> [extra_tag]
  local dir="$1" img="$2" extra="${3:-}"
  if [ -n "${MULTIARCH:-}" ]; then
    docker buildx build --platform linux/amd64,linux/arm64 \
      -f "$dir/Containerfile" -t "$REG/$img" ${extra:+-t "$REG/$extra"} --push "$dir"
  else
    docker build --platform linux/arm64 -f "$dir/Containerfile" -t "$REG/$img" "$dir"
    docker push "$REG/$img"
    if [ -n "$extra" ]; then docker tag "$REG/$img" "$REG/$extra"; docker push "$REG/$extra"; fi
  fi
}

#build_push dcs-workshop-base dcs-workshop-base:dev
#build_push hello-dcs hello-dcs:dev samples/hello-dcs:1.0
build_push dcs-academy-portal dcs-academy-portal:dev
echo "done -> $REG/{dcs-workshop-base:dev, hello-dcs:dev, samples/hello-dcs:1.0, feedback-collector:dev, dcs-academy-portal:dev}"
