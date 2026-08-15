from application.config.llm_config import LLMConfig
from application.config.settings import Settings
from application.ports.llm_port import LLMPort

from infrastructure.llm.llm_factory import create_llm


def build_llm(settings: Settings) -> LLMPort:

    config = LLMConfig(
        provider=settings.llm_provider,
        model=settings.llm_model,
        api_key=settings.gemini_api_key,
        host=settings.ollama_host,
    )

    return create_llm(config)