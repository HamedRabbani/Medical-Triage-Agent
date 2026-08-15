from application.contracts.llm_risk_assessment import (
    LLMRiskAssessment,
)
from agents.risk_agent import risk_agent


class FakeLLMService:

    def generate_structured(
        self,
        prompt,
        response_model,
        *,
        system_prompt=None,
    ):
        return LLMRiskAssessment(
            risk_level="LOW",
            confidence=0.99,
            red_flags=[],
            recommendation="Low risk.",
        )


def test_rule_engine_remains_safety_baseline():

    state = {
        "symptoms": [
            "chest pain",
            "shortness of breath",
        ],
        "severity": None,
        "age": None,
        "duration": None,
        "red_flags": [],
    }

    result = risk_agent(
        state,
        llm_service=FakeLLMService(),
    )

    # Rule Engine must remain authoritative
    assert result["risk_level"] == "HIGH"

    # LLM result is preserved separately
    assert result["llm_risk_level"] == "LOW"

    assert result["risk_level"] != result["llm_risk_level"]