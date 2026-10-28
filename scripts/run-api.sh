#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ ! -x "${ROOT}/.venv/bin/python" ]]; then
  echo "Run: make install" >&2
  exit 1
fi
export PYTHONPATH="${ROOT}/core:${ROOT}/api"
RELOAD="${BOTOS_RELOAD:-false}"
if [[ "${RELOAD}" == "true" ]]; then
  exec .venv/bin/uvicorn botos_api.main:app --host "${BOTOS_HOST:-0.0.0.0}" --port "${BOTOS_PORT:-8000}" --reload
fi
exec .venv/bin/uvicorn botos_api.main:app --host "${BOTOS_HOST:-0.0.0.0}" --port "${BOTOS_PORT:-8000}"
