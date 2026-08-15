from application.contracts.llm_test_response import LLMTestResponse
from application.ports.llm_port import LLMPort


def verify_llm_contract(llm: LLMPort) -> None:
    result = llm.generate(
        "Say hello in one sentence."
    )

    assert isinstance(result, str)
    assert result.strip()


def test_llm_generate_contract():
    class FakeLLM(LLMPort):
        def generate(self, prompt: str, *, system_prompt=None) -> str:
            return "Hello"

        def generate_structured(
            self,
            prompt: str,
            response_model,
            *,
            system_prompt=None,
        ):
            return response_model(
                symptoms=["headache"]
            )

    llm = FakeLLM()

    verify_llm_contract(llm)

    result = llm.generate_structured(
        "Extract symptoms.",
        LLMTestResponse,
    )

    assert isinstance(result, LLMTestResponse)
    assert result.symptoms == ["headache"]


def test_llm_structured_contract():
    class FakeLLM(LLMPort):
        def generate(self, prompt: str, *, system_prompt=None) -> str:
            return "Hello"

        def generate_structured(
            self,
            prompt: str,
            response_model,
            *,
            system_prompt=None,
        ):
            return response_model(
                symptoms=["fever", "headache"]
            )

    result = FakeLLM().generate_structured(
        "Extract symptoms.",
        LLMTestResponse,
    )

    assert result.symptoms == ["fever", "headache"]