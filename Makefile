.PHONY: help api core check install

help:
	@echo "BotOS dev targets:"
	@echo "  make install  - venv + pip install"
	@echo "  make api      - run FastAPI on :8000"
	@echo "  make core     - run Discord core bot"
	@echo "  make check    - ruff check core api"

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements-dev.txt

api:
	PYTHONPATH=core:api .venv/bin/python -m botos_api.main

core:
	PYTHONPATH=core:api .venv/bin/python -m botos_core.main

check:
	.venv/bin/ruff check core api
