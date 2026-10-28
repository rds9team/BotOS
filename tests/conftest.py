"""Pytest hooks for BotOS."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _botos_test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    from botos_api.db.session import reset_engine_for_tests

    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    reset_engine_for_tests()
    yield
    reset_engine_for_tests()
