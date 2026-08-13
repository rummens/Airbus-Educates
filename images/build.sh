#!/usr/bin/env bash
# Build + push the DCS Academy images to the GitHub Container Registry.
#
#   ./build.sh                    # all images, arm64 (CRC target), the default
#   ./build.sh dcs-ci             # only that one image
#   MULTIARCH=1 ./build.sh        # amd64 + arm64 via buildx (for x86 clusters too)
#
# Requires: docker logged in to ghcr.io (write:packages) and to the Red Hat
# registry (for the UBI base of hello-dcs). After first push, make the packages
# public in GitHub for unauthenticated cluster pulls.
set -euo pipefail
REG="${REG:-ghcr.io/rummens}"
MULTIARCH="${MULTIARCH:-1}"
cd "$(dirname "$0")"

known_dirs=()
built=()
target="${1:-}"

build_push() {           # <dir> <image> [extra_tag] [context]
  local dir="$1" img="$2" extra="${3:-}" ctx="${4:-$1}"
  known_dirs+=("$dir")
  [ -n "$target" ] && [ "$dir" != "$target" ] && return 0
  if [ -n "${MULTIARCH:-}" ]; then
    echo "Building Multiarch"
    docker buildx build --platform linux/amd64,linux/arm64 \
      -f "$dir/Containerfile" -t "$REG/$img" ${extra:+-t "$REG/$extra"} --push "$ctx"
  else
    echo "Buidling ARM only"
    docker build --platform linux/arm64 -f "$dir/Containerfile" -t "$REG/$img" "$ctx"
    docker push "$REG/$img"
    if [ -n "$extra" ]; then docker tag "$REG/$img" "$REG/$extra"; docker push "$REG/$extra"; fi
  fi
  built+=("$REG/$img")
}

build_push dcs-workshop-base dcs-workshop-base:develop
build_push hello-dcs hello-dcs:dev samples/hello-dcs:1.0
build_push dcs-academy-portal dcs-academy-portal:dev
build_push educates-mirror educates-mirror:dev
# Context is images/ (not images/dcs-ci): the CI image bakes the portal's
# requirements.txt so air-gapped runners pip-install nothing.
build_push dcs-ci dcs-ci:dev "" .

if [ -n "$target" ] && [ "${#built[@]}" -eq 0 ]; then
  echo "no such image dir: $target (known: ${known_dirs[*]})" >&2
  exit 1
fi
echo "done -> ${built[*]}"
