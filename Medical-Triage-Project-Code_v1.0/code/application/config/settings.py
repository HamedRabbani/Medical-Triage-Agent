# application/config/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    llm_provider: str = "ollama"
    llm_model: str = "gemma3"
    gemini_api_key: str | None = None
    ollama_host: str = "http://localhost:11434"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )