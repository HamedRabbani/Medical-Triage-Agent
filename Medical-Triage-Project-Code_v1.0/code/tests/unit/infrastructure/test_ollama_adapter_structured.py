from application.contracts.llm_risk_assessment import (
    LLMRiskAssessment,
)
from infrastructure.llm.ollama_adapter import OllamaAdapter


class FakeMessage:
    def __init__(self, content: str):
        self.content = content


class FakeResponse:
    def __init__(self, content: str):
        self.message = FakeMessage(content)


class FakeClient:
    def chat(self, **kwargs):
        return FakeResponse(
            """
            {
                "risk_level": "HIGH",
                "confidence": 0.95,
                "red_flags": ["chest pain"],
                "recommendation": "Immediate evaluation required."
            }
            """
        )


def test_ollama_structured_output():
    adapter = OllamaAdapter(model="test-model")

    adapter._client = FakeClient()

    result = adapter.generate_structured(
        prompt="Patient has chest pain.",
        response_model=LLMRiskAssessment,
    )

    assert isinstance(result, LLMRiskAssessment)
    assert result.risk_level == "HIGH"
    assert result.confidence == 0.95
    assert "chest pain" in result.red_flags