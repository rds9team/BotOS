"""Configuration loaded from environment (see repo `.env.example`)."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from botos_core.repo_root import repo_root


class CoreSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(repo_root() / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    discord_bot_token: str = ""
    database_url: str = "sqlite+aiosqlite:///data/botos.db"
    sync_global_commands_on_ready: bool = False

    @field_validator("discord_bot_token")
    @classmethod
    def strip_token(cls, value: str) -> str:
        return value.strip()

    @field_validator("database_url")
    @classmethod
    def database_url_not_blank(cls, value: str) -> str:
        if not value.strip():
            msg = "DATABASE_URL must not be empty"
            raise ValueError(msg)
        return value.strip()


def load_settings() -> CoreSettings:
    return CoreSettings()
