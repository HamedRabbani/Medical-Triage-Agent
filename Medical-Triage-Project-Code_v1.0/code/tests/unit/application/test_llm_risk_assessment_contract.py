import pytest
from pydantic import ValidationError

from application.contracts.llm_risk_assessment import (
    LLMRiskAssessment,
)


def test_valid_llm_risk_assessment():
    result = LLMRiskAssessment(
        risk_level="HIGH",
        confidence=1.0,
        red_flags=["chest pain with shortness of breath"],
        recommendation="Immediate evaluation required.",
    )

    assert result.risk_level == "HIGH"
    assert result.confidence == 1.0
    assert result.red_flags
    assert result.recommendation


def test_confidence_must_be_between_zero_and_one():
    with pytest.raises(ValidationError):
        LLMRiskAssessment(
            risk_level="HIGH",
            confidence=1.1,
            red_flags=[],
            recommendation="Immediate evaluation required.",
        )


def test_invalid_risk_level_is_rejected():
    with pytest.raises(ValidationError):
        LLMRiskAssessment(
            risk_level="MEDIUM",
            confidence=0.8,
            red_flags=[],
            recommendation="Evaluation required.",
        )


def test_red_flags_default_to_empty_list():
    result = LLMRiskAssessment(
        risk_level="LOW",
        confidence=0.8,
        recommendation="No immediate concern.",
    )

    assert result.red_flags == []