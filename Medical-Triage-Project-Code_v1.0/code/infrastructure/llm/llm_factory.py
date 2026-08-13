from application.config.llm_config import LLMConfig
from application.ports.llm_port import LLMPort

from infrastructure.llm.gemini_adapter import GeminiAdapter
from infrastructure.llm.ollama_adapter import OllamaAdapter


def create_llm(config: LLMConfig) -> LLMPort:

    if config.provider == "gemini":
        if not config.api_key:
            raise ValueError("Gemini API key is required.")

        return GeminiAdapter(
            api_key=config.api_key,
            model=config.model,
        )

    if config.provider == "ollama":
        return OllamaAdapter(
            model=config.model,
            host=config.host or "http://localhost:11434",
        )

    raise ValueError(
        f"Unsupported LLM provider: {config.provider}"
    )