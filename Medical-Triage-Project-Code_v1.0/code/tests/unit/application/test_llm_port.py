from pydantic import BaseModel

from application.ports.llm_port import LLMPort


class FakeResponse(BaseModel):
    answer: str


class FakeLLM(LLMPort):

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:
        return f"Fake response: {prompt}"

    def generate_structured(
        self,
        prompt: str,
        response_model: type[FakeResponse],
        *,
        system_prompt: str | None = None,
    ) -> FakeResponse:
        return response_model(
            answer=f"Structured response: {prompt}"
        )


def test_llm_port_contract():
    llm = FakeLLM()

    result = llm.generate("Hello")

    assert result == "Fake response: Hello"


def test_llm_port_structured_contract():
    llm = FakeLLM()

    result = llm.generate_structured(
        "Hello",
        FakeResponse,
    )

    assert isinstance(result, FakeResponse)
    assert result.answer == "Structured response: Hello"