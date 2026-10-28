"""Guild and plugin HTTP API — paths follow `docs/architecture.md`."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/api/guilds", tags=["guilds"])


@router.get("")
async def list_guilds() -> dict[str, list]:
    """TODO: Discord OAuth + user guilds."""
    return {"guilds": []}


@router.get("/{guild_id}/plugins")
async def list_guild_plugins(guild_id: str) -> dict[str, str | list]:
    return {"guild_id": guild_id, "plugins": []}


@router.post("/{guild_id}/plugins/{plugin_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def upsert_guild_plugin(guild_id: str, plugin_id: str) -> None:
    """Save plugin JSON and request core sync (not wired)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Plugin upsert for guild={guild_id} plugin={plugin_id} not implemented",
    )
