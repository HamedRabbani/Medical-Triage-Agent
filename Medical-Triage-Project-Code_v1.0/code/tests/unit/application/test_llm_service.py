from application.contracts.llm_test_response import LLMTestResponse
from application.services.llm_service import LLMService


class FakeLLM:

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:
        return "fake response"

    def generate_structured(
        self,
        prompt: str,
        response_model,
        *,
        system_prompt: str | None = None,
    ):
        return response_model(
            symptoms=["headache"]
        )


def test_llm_service_generate():
    service = LLMService(FakeLLM())

    result = service.generate("Hello")

    assert result == "fake response"


def test_llm_service_generate_structured():
    service = LLMService(FakeLLM())

    result = service.generate_structured(
        "Extract symptoms",
        LLMTestResponse,
    )

    assert isinstance(result, LLMTestResponse)
    assert result.symptoms == ["headache"]