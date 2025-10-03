"""Configuration helpers for the Telegram monitoring agent."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Runtime configuration for the monitoring workflow."""

    telegram_chat_id: str = Field(..., alias="TELEGRAM_CHAT_ID")
    telegram_server_url: str = Field(..., alias="TELEGRAM_MCP_SERVER")
    telegram_api_key: Optional[str] = Field(default=None, alias="TELEGRAM_MCP_API_KEY")

    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    summary_model: str = Field("gpt-4o-mini", alias="OPENAI_SUMMARY_MODEL")
    image_model: str = Field("gpt-image-1", alias="OPENAI_IMAGE_MODEL")

    backend_base_url: str = Field("http://localhost:8000", alias="BACKEND_BASE_URL")
    state_file: Path = Field(Path("agent_state.json"), alias="AGENT_STATE_FILE")
    request_timeout: int = Field(20, alias="REQUEST_TIMEOUT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True


settings = Settings()
