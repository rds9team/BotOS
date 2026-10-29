"""FastAPI application factory."""

from __future__ import annotations

import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.engine import make_url

from botos_api.auth import router as auth_router
from botos_api.db.models import Base
from botos_api.db.session import dispose_engine, get_engine
from botos_api.routes import guilds, health


def _ensure_sqlite_parent_dir(database_url: str) -> None:
    url = make_url(database_url)
    if not url.drivername.startswith("sqlite"):
        return
    database = url.database
    if not database or database == ":memory:":
        return
    Path(database).expanduser().parent.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from botos_api.config import load_settings

    settings = load_settings()
    _ensure_sqlite_parent_dir(settings.database_url)

    health.set_started_at(time.time())

    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from sqlalchemy.ext.asyncio import async_sessionmaker

    from botos_api.services.plugin_catalog import sync_standard_plugins_to_db

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        await sync_standard_plugins_to_db(session)

    yield
    await dispose_engine()


def create_app() -> FastAPI:
    from botos_api.config import load_settings

    settings = load_settings()
    app = FastAPI(title="BotOS API", version="0.0.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.state.botos_settings = settings

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    @app.exception_handler(ValueError)
    async def value_error_handler(_request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    app.include_router(health.router)
    app.include_router(auth_router)
    app.include_router(guilds.router)

    from botos_api.repo_root import repo_root

    web_dir = repo_root() / "web"
    if web_dir.is_dir():
        app.mount("/", StaticFiles(directory=web_dir, html=True), name="web")
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
        reload=settings.botos_reload,
    )


if __name__ == "__main__":
    main()
