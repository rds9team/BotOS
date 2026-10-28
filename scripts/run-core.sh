#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ ! -x "${ROOT}/.venv/bin/python" ]]; then
  echo "Run: make install" >&2
  exit 1
fi
export PYTHONPATH="${ROOT}/core:${ROOT}/api"
exec .venv/bin/python -m botos_core.main
