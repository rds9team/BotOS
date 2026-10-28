.PHONY: help api core check test install

help:
	@echo "BotOS dev targets:"
	@echo "  make install  - venv + pip install"
	@echo "  make api      - run FastAPI on :8000"
	@echo "  make core     - run Discord core bot"
	@echo "  make check    - ruff check core api tests"
	@echo "  make test     - pytest"

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements-dev.txt

api:
	@test -x .venv/bin/python || (echo "Run: make install" && exit 1)
	PYTHONPATH=core:api .venv/bin/python -m botos_api.main

core:
	@test -x .venv/bin/python || (echo "Run: make install" && exit 1)
	PYTHONPATH=core:api .venv/bin/python -m botos_core.main

check:
	@test -x .venv/bin/ruff || (echo "Run: make install" && exit 1)
	.venv/bin/ruff check core api tests

test: check
	@test -x .venv/bin/pytest || (echo "Run: make install" && exit 1)
	PYTHONPATH=core:api .venv/bin/pytest -q
