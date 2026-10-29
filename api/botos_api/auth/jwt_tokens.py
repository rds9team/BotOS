"""JWT issue and verify."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from botos_api.config import load_settings


def create_access_token(*, user_id: str, discord_id: str) -> str:
    settings = load_settings()
    now = datetime.now(tz=UTC)
    payload = {
        "sub": user_id,
        "discord_id": discord_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_expires_minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any]:
    settings = load_settings()
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
