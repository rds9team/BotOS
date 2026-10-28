"""Configuration loaded from environment (see repo `.env.example`)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class CoreSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    discord_bot_token: str = ""
    database_url: str = "sqlite+aiosqlite:///data/botos.db"


def load_settings() -> CoreSettings:
    return CoreSettings()
