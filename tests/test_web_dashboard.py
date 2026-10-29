"""Tests for the web dashboard wiring (WEB-02): oauth web flow and static UI."""

from __future__ import annotations

from fastapi.testclient import TestClient

from botos_api.auth.discord_oauth import create_oauth_state, state_kind, verify_oauth_state
from botos_api.main import create_app


def test_static_dashboard_is_served() -> None:
    client = TestClient(create_app())
    res = client.get("/")
    assert res.status_code == 200
    assert "BotOS Dashboard" in res.text
    assert 'src="app.js"' in res.text
    css = client.get("/style.css")
    assert css.status_code == 200
    js = client.get("/app.js")
    assert js.status_code == 200
    assert "/api/guilds" in js.text


def test_oauth_state_kinds() -> None:
    assert state_kind(create_oauth_state(kind="web")) == "web"
    assert state_kind(create_oauth_state(kind="api")) == "api"
    assert verify_oauth_state(create_oauth_state(kind="web")) is True
    assert verify_oauth_state("tampered") is False


def test_api_routes_take_precedence_over_static_mount() -> None:
    client = TestClient(create_app())
    assert client.get("/api/health").status_code == 200
    unknown = client.get("/api/unknown-path")
    assert unknown.status_code in {404, 405}
