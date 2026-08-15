from unittest.mock import Mock

from agents.risk_agent import risk_agent
from application.contracts.llm_risk_assessment import (
    LLMRiskAssessment,
)


def test_risk_agent_high_risk():

    state = {
        "symptoms": [
            "chest pain",
            "shortness of breath",
        ],
        "severity": "moderate",
        "age": 35,
        "duration": "1 day",
    }

    fake_llm_result = LLMRiskAssessment(
        risk_level="HIGH",
        confidence=0.95,
        red_flags=[
            "chest pain with shortness of breath"
        ],
        recommendation="Emergency evaluation is required.",
    )

    mock_llm_service = Mock()

    mock_llm_service.generate_structured.return_value = (
        fake_llm_result
    )

    result = risk_agent(
        state,
        llm_service=mock_llm_service,
    )

    # Rule Engine
    assert result["risk_level"] == "HIGH"

    # LLM
    assert result["llm_risk_level"] == "HIGH"
    assert result["llm_confidence"] == 0.95
    assert result["llm_red_flags"] == [
        "chest pain with shortness of breath"
    ]
    assert (
        result["llm_recommendation"]
        == "Emergency evaluation is required."
    )

    # Verify LLM was called
    mock_llm_service.generate_structured.assert_called_once()


def test_risk_agent_severe():

    state = {
        "symptoms": ["headache"],
        "severity": "severe",
        "age": 35,
        "duration": "2 days",
    }

    fake_llm_result = LLMRiskAssessment(
        risk_level="HIGH",
        confidence=0.90,
        red_flags=[],
        recommendation="Prompt medical evaluation is recommended.",
    )

    mock_llm_service = Mock()

    mock_llm_service.generate_structured.return_value = (
        fake_llm_result
    )

    result = risk_agent(
        state,
        llm_service=mock_llm_service,
    )

    # Rule Engine
    assert result["risk_level"] == "HIGH"

    # LLM
    assert result["llm_risk_level"] == "HIGH"
    assert result["llm_confidence"] == 0.90
    assert result["llm_red_flags"] == []
    assert (
        result["llm_recommendation"]
        == "Prompt medical evaluation is recommended."
    )

    mock_llm_service.generate_structured.assert_called_once()


def test_risk_agent_low_risk():

    state = {
        "symptoms": ["headache"],
        "severity": "mild",
        "age": 35,
        "duration": "1 day",
    }

    fake_llm_result = LLMRiskAssessment(
        risk_level="LOW",
        confidence=0.80,
        red_flags=[],
        recommendation="Continue monitoring symptoms.",
    )

    mock_llm_service = Mock()

    mock_llm_service.generate_structured.return_value = (
        fake_llm_result
    )

    result = risk_agent(
        state,
        llm_service=mock_llm_service,
    )

    # Rule Engine
    assert result["risk_level"] == "LOW"

    # LLM
    assert result["llm_risk_level"] == "LOW"
    assert result["llm_confidence"] == 0.80
    assert result["llm_red_flags"] == []
    assert (
        result["llm_recommendation"]
        == "Continue monitoring symptoms."
    )

    mock_llm_service.generate_structured.assert_called_once()