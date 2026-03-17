#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

ENV_FILE="${ENV_FILE:-.env}"
export UV_CACHE_DIR="${UV_CACHE_DIR:-$SCRIPT_DIR/.uv-cache}"
export UV_TOOL_DIR="${UV_TOOL_DIR:-$SCRIPT_DIR/.uv-tools}"
mkdir -p "$UV_CACHE_DIR"
mkdir -p "$UV_TOOL_DIR"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

export TWINE_USERNAME="${TWINE_USERNAME:-__token__}"

if [[ -z "${TWINE_PASSWORD:-}" ]]; then
  echo "Error: TWINE_PASSWORD is not set. Put it in $ENV_FILE or export it." >&2
  exit 1
fi

if ! compgen -G "dist/*" > /dev/null; then
  echo "Error: no files found in dist/. Build first (e.g. python3 -m build --no-isolation)." >&2
  exit 1
fi

echo "Uploading distributions from dist/ to PyPI..."
uvx twine upload --non-interactive "$@" dist/*
