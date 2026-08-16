import os

from dotenv import load_dotenv

from application.config.llm_config import LLMConfig


load_dotenv()


def load_llm_config() -> LLMConfig:
    """
    Load LLM configuration from environment variables.
    """

    provider = os.getenv(
        "LLM_PROVIDER",
        "gemini",
    )

    model = os.getenv(
        "LLM_MODEL",
        "gemini-2.5-flash",
    )

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

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