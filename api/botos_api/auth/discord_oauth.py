"""Discord OAuth2 helpers."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from urllib.parse import urlencode

import httpx
import jwt
from jwt import InvalidTokenError

from botos_api.config import load_settings

DISCORD_API = "https://discord.com/api/v10"
OAUTH_SCOPES = "identify guilds"


def build_authorize_url(*, state: str) -> str:
    settings = load_settings()
    if not settings.discord_client_id:
        msg = "DISCORD_CLIENT_ID is not configured"
        raise ValueError(msg)
    params = {
        "client_id": settings.discord_client_id,
        "redirect_uri": settings.discord_redirect_uri,
        "response_type": "code",
        "scope": OAUTH_SCOPES,
        "state": state,
        "prompt": "consent",
    }
    return f"https://discord.com/oauth2/authorize?{urlencode(params)}"


def create_oauth_state() -> str:
    settings = load_settings()
    now = datetime.now(tz=UTC)
    payload = {
        "purpose": "oauth_state",
        "exp": int((now + timedelta(minutes=10)).timestamp()),
        "iat": int(now.timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def verify_oauth_state(state: str) -> bool:
    settings = load_settings()
    try:
        payload = jwt.decode(state, settings.jwt_secret, algorithms=["HS256"])
    except InvalidTokenError:
        return False
    return payload.get("purpose") == "oauth_state"


async def exchange_code(code: str) -> dict[str, Any]:
    settings = load_settings()
    data = {
        "client_id": settings.discord_client_id,
        "client_secret": settings.discord_client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.discord_redirect_uri,
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(f"{DISCORD_API}/oauth2/token", data=data)
        response.raise_for_status()
        return response.json()


async def fetch_current_user(access_token: str) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            f"{DISCORD_API}/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        return response.json()


async def fetch_user_guilds(access_token: str) -> list[dict[str, Any]]:
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            f"{DISCORD_API}/users/@me/guilds",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            return []
        return payload
