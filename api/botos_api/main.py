"""FastAPI application factory."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from botos_api.db.models import Base
from botos_api.db.session import get_engine
from botos_api.routes import guilds, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    from botos_api.config import load_settings

    settings = load_settings()
    if settings.database_url.startswith("sqlite"):
        # Ensure parent dir exists for file-based SQLite (see `.env.example`).
        path_part = settings.database_url.split("///", 1)[-1]
        if path_part and path_part != ":memory:":
            Path(path_part).parent.mkdir(parents=True, exist_ok=True)

    engine: AsyncEngine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="BotOS API", version="0.0.0", lifespan=lifespan)
    app.include_router(health.router)
    app.include_router(guilds.router)
    return app


app = create_app()


def main() -> None:
    import uvicorn

    from botos_api.config import load_settings

    settings = load_settings()
    uvicorn.run(
        "botos_api.main:app",
        host=settings.botos_host,
        port=settings.botos_port,
        reload=True,
    )


if __name__ == "__main__":
    main()
