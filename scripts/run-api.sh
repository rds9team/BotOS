#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/core:${ROOT}/api"
exec .venv/bin/uvicorn botos_api.main:app --host "${BOTOS_HOST:-0.0.0.0}" --port "${BOTOS_PORT:-8000}" --reload
