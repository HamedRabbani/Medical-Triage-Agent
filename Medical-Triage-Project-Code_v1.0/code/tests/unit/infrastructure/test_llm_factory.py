import pytest

from application.config.llm_config import LLMConfig
from infrastructure.llm.llm_factory import create_llm
from infrastructure.llm.gemini_adapter import GeminiAdapter
from infrastructure.llm.ollama_adapter import OllamaAdapter


def test_create_gemini_adapter():

    config = LLMConfig(
        provider="gemini",
        model="test-model",
        api_key="test-key",
    )

    llm = create_llm(config)

    assert isinstance(llm, GeminiAdapter)


def test_create_ollama_adapter():

    config = LLMConfig(
        provider="ollama",
        model="test-model",
    )

    llm = create_llm(config)

    assert isinstance(llm, OllamaAdapter)


def test_unsupported_provider():

    config = LLMConfig(
        provider="unknown",
        model="test-model",
    )

    with pytest.raises(ValueError):
        create_llm(config)