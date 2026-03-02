"""Settings loaded from .env via pydantic-settings."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    YOUTUBE_API_KEY: str = Field(..., description="YouTube Data API v3 key")
    DATA_DIR: Path = Field(Path("data"), description="Root directory for channel data")
    LOGS_DIR: Path = Field(Path("logs"), description="Directory for log files")
    YTCHAN_PROXY: str | None = Field(None, description="Optional HTTP/S proxy URL")
    YTCHAN_COOKIES_BROWSER: str = Field("none", description="Browser to pull cookies from (chrome/firefox/edge/brave). Set to 'none' to disable.")
    YTCHAN_COOKIES_FILE: str | None = Field(None, description="Path to a Netscape cookies.txt file exported from your browser.")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
