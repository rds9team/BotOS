"""Guild and plugin HTTP API — paths follow `docs/architecture.md`."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from botos_api.validation import validate_guild_id_param, validate_plugin_id_param

router = APIRouter(prefix="/api/guilds", tags=["guilds"])


def _http_error(status_code: int, detail: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail=detail)


@router.get("/")
async def list_guilds() -> dict[str, list]:
    """TODO: Discord OAuth + user guilds."""
    return {"guilds": []}


@router.get("/{guild_id}/plugins")
async def list_guild_plugins(guild_id: str) -> dict[str, str | list]:
    if err := validate_guild_id_param(guild_id):
        raise _http_error(status.HTTP_422_UNPROCESSABLE_CONTENT, err)
    return {"guild_id": guild_id, "plugins": []}


@router.post("/{guild_id}/plugins/{plugin_id}")
async def upsert_guild_plugin(guild_id: str, plugin_id: str) -> None:
    """Save plugin JSON and request core sync (not wired)."""
    if err := validate_guild_id_param(guild_id):
        raise _http_error(status.HTTP_422_UNPROCESSABLE_CONTENT, err)
    if err := validate_plugin_id_param(plugin_id):
        raise _http_error(status.HTTP_422_UNPROCESSABLE_CONTENT, err)
    raise _http_error(
        status.HTTP_501_NOT_IMPLEMENTED,
        f"Plugin upsert for guild={guild_id} plugin={plugin_id} not implemented",
    )
