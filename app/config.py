from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"

    database_url: str | None = None

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    sec_user_agent: str = "FinAssistant MVP contact@example.com"
    news_api_key: str | None = None

    cache_ttl_seconds: int = 3600


@lru_cache
def get_settings() -> Settings:
    return Settings()
