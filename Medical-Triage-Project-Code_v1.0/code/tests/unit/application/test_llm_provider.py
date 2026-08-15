from application.config.llm_provider import build_llm
from application.config.settings import Settings
from infrastructure.llm.ollama_adapter import OllamaAdapter


def test_build_ollama_llm():

    settings = Settings(
        llm_provider="ollama",
        llm_model="gemma3",
        ollama_host="http://localhost:11434",
    )

    llm = build_llm(settings)

    assert isinstance(llm, OllamaAdapter)