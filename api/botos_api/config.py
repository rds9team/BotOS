"""API settings from environment."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    botos_host: str = "0.0.0.0"
    botos_port: int = 8000
    database_url: str = "sqlite+aiosqlite:///data/botos.db"
    jwt_secret: str = "replace_this_with_a_secure_random_key"


def load_settings() -> ApiSettings:
    return ApiSettings()
