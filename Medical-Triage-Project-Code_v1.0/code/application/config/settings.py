from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    # =========================================================
    # LLM
    # =========================================================

    llm_provider: str = "ollama"
    llm_model: str = "gemma3:latest"

    gemini_api_key: str | None = None

    ollama_host: str = (
        "http://localhost:11434"
    )

    # =========================================================
    # Database
    # =========================================================

    db_backend: str = "sqlserver"

    database_url: str | None = None

    supabase_url: str | None = None
    supabase_key: str | None = None

    # =========================================================
    # Configuration
    # =========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )