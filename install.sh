#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
INSTALLER="$ROOT_DIR/scripts/install.py"

if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 8))' >/dev/null 2>&1; then
  PYTHON=(python3)
elif command -v python >/dev/null 2>&1 && python -c 'import sys; raise SystemExit(sys.version_info < (3, 8))' >/dev/null 2>&1; then
  PYTHON=(python)
elif command -v py >/dev/null 2>&1 && py -3 -c 'import sys; raise SystemExit(sys.version_info < (3, 8))' >/dev/null 2>&1; then
  PYTHON=(py -3)
else
  echo "Security Coverage installer requires Python 3.8 or newer." >&2
  exit 127
fi

exec "${PYTHON[@]}" "$INSTALLER" "$@"
