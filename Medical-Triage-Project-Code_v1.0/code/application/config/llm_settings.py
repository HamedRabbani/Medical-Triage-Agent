import os

from application.config.llm_config import LLMConfig


def load_llm_config() -> LLMConfig:
    provider = os.getenv("LLM_PROVIDER", "ollama")
    model = os.getenv("LLM_MODEL", "gemma3")

    api_key = os.getenv("GEMINI_API_KEY")
    host = os.getenv(
        "OLLAMA_HOST",
        "http://localhost:11434",
    )

    return LLMConfig(
        provider=provider,
        model=model,
        api_key=api_key,
        host=host,
    )