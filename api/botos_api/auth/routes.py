"""Auth routes."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from botos_api.auth.deps import AuthenticatedUser, get_current_user
from botos_api.auth.discord_oauth import (
    build_authorize_url,
    create_oauth_state,
    exchange_code,
    fetch_current_user,
    fetch_user_guilds,
    state_kind,
    verify_oauth_state,
)
from botos_api.auth.jwt_tokens import create_access_token
from botos_api.db.models import User, UserOAuthToken
from botos_api.db.session import get_session

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _manageable_guilds(raw_guilds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    manageable: list[dict[str, Any]] = []
    for guild in raw_guilds:
        permissions = int(guild.get("permissions", 0))
        if permissions & 0x20:
            manageable.append(
                {
                    "id": str(guild.get("id")),
                    "name": str(guild.get("name", "")),
                    "icon": guild.get("icon"),
                }
            )
    return manageable


@router.get("/discord/login")
async def discord_login(kind: str = Query(default="api", pattern="^(api|web)$")) -> dict[str, str]:
    state = create_oauth_state(kind=kind)
    return {"authorize_url": build_authorize_url(state=state), "state": state}


@router.get("/discord/callback")
async def discord_callback(
    code: str = Query(...),
    state: str = Query(...),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    if not verify_oauth_state(state):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OAuth state")

    token_payload = await exchange_code(code)
    discord_access = str(token_payload.get("access_token", ""))
    if not discord_access:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token exchange failed")

    profile = await fetch_current_user(discord_access)
    discord_id = str(profile.get("id", ""))
    username = str(profile.get("username", "unknown"))
    avatar = profile.get("avatar")
    avatar_url = (
        f"https://cdn.discordapp.com/avatars/{discord_id}/{avatar}.png" if avatar else None
    )

    user = await session.scalar(select(User).where(User.discord_id == discord_id))
    if user is None:
        user = User(
            id=str(uuid.uuid4()),
            discord_id=discord_id,
            username=username,
            avatar_url=avatar_url,
        )
        session.add(user)
        await session.flush()
    else:
        user.username = username
        user.avatar_url = avatar_url

    expires_in = int(token_payload.get("expires_in", 604800))
    oauth_row = await session.get(UserOAuthToken, user.id)
    if oauth_row is None:
        oauth_row = UserOAuthToken(user_id=user.id, access_token=discord_access)
        session.add(oauth_row)
    else:
        oauth_row.access_token = discord_access
    oauth_row.refresh_token = token_payload.get("refresh_token")
    oauth_row.expires_at = datetime.now(tz=UTC) + timedelta(seconds=expires_in)

    guilds = _manageable_guilds(await fetch_user_guilds(discord_access))
    jwt_token = create_access_token(user_id=user.id, discord_id=user.discord_id)
    await session.commit()

    if state_kind(state) == "web":
        from botos_api.config import load_settings

        fragment = f"token={jwt_token}"
        frontend = load_settings().botos_frontend_url.rstrip("/")
        return RedirectResponse(f"{frontend}/#{fragment}", status_code=302)

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": {"id": user.id, "discord_id": discord_id, "username": username},
        "guilds": guilds,
    }


@router.get("/me")
async def auth_me(user: AuthenticatedUser = Depends(get_current_user)) -> dict[str, str]:
    return {"id": user.id, "discord_id": user.discord_id, "username": user.username}
