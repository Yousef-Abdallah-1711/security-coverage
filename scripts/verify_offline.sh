#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
image_tag="${SECURITY_COVERAGE_OFFLINE_IMAGE:-security-coverage-offline-check:local}"
docker_source="$repo_root"
docker_file="$repo_root/tests/docker/offline-check.Dockerfile"

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*)
    docker_source="$(cygpath -m "$repo_root")"
    docker_file="$(cygpath -m "$docker_file")"
    export MSYS_NO_PATHCONV=1
    ;;
esac

docker build --file "$docker_file" --tag "$image_tag" "$docker_source"
docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --mount "type=bind,src=$docker_source,dst=/workspace,readonly" \
  --tmpfs /tmp:rw,noexec,nosuid,size=32m \
  "$image_tag" \
  python /workspace/scripts/verify_offline.py
