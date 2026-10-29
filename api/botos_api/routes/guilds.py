"""Guild and plugin HTTP API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from botos_api.auth.deps import AuthenticatedUser, get_current_user
from botos_api.auth.discord_oauth import fetch_user_guilds
from botos_api.db.models import UserOAuthToken
from botos_api.db.session import get_session
from botos_api.services.guild_plugins import install_guild_plugin, list_guild_plugins
from botos_api.validation import validate_guild_id_param, validate_plugin_id_param
from botos_core.plugin_manager import PluginManager

router = APIRouter(prefix="/api/guilds", tags=["guilds"])


class InstallPluginBody(BaseModel):
    guild_name: str = Field(default="Unknown", max_length=100)


def _http_error(status_code: int, detail: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail=detail)


async def _user_can_manage_guild(
    session: AsyncSession,
    user: AuthenticatedUser,
    guild_id: str,
) -> bool:
    token_row = await session.get(UserOAuthToken, user.id)
    if token_row is None:
        return False
    guilds = await fetch_user_guilds(token_row.access_token)
    for guild in guilds:
        if str(guild.get("id")) != guild_id:
            continue
        permissions = int(guild.get("permissions", 0))
        return bool(permissions & 0x20)
    return False


@router.get("/")
async def list_guilds(
    user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict[str, list]:
    token_row = await session.get(UserOAuthToken, user.id)
    if token_row is None:
        return {"guilds": []}
    raw = await fetch_user_guilds(token_row.access_token)
    manageable = []
    for guild in raw:
        permissions = int(guild.get("permissions", 0))
        if permissions & 0x20:
            manageable.append(
                {
                    "id": str(guild.get("id")),
                    "name": str(guild.get("name", "")),
                    "icon": guild.get("icon"),
                }
            )
    return {"guilds": manageable}


@router.get("/{guild_id}/plugins")
async def list_guild_plugins_route(
    guild_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    if err := validate_guild_id_param(guild_id):
        raise _http_error(status.HTTP_422_UNPROCESSABLE_CONTENT, err)
    if not await _user_can_manage_guild(session, user, guild_id):
        raise _http_error(status.HTTP_403_FORBIDDEN, detail="Forbidden")
    plugins = await list_guild_plugins(session, guild_id)
    return {"guild_id": guild_id, "plugins": plugins}


@router.post("/{guild_id}/plugins/{plugin_id}")
async def upsert_guild_plugin(
    guild_id: str,
    plugin_id: str,
    body: InstallPluginBody,
    user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    if err := validate_guild_id_param(guild_id):
        raise _http_error(status.HTTP_422_UNPROCESSABLE_CONTENT, err)
    if err := validate_plugin_id_param(plugin_id):
        raise _http_error(status.HTTP_422_UNPROCESSABLE_CONTENT, err)
    if not await _user_can_manage_guild(session, user, guild_id):
        raise _http_error(status.HTTP_403_FORBIDDEN, detail="Forbidden")

    manager = PluginManager()
    manager.discover_standard_plugins()
    found = manager.get(plugin_id)
    if found is None:
        raise _http_error(status.HTTP_404_NOT_FOUND, detail="Plugin not found in catalog")
    manifest = found.raw

    await install_guild_plugin(
        session,
        guild_id=guild_id,
        plugin_id=plugin_id,
        manifest=manifest,
        guild_name=body.guild_name,
    )
    await session.commit()
    return {"status": "installed", "guild_id": guild_id, "plugin_id": plugin_id}
