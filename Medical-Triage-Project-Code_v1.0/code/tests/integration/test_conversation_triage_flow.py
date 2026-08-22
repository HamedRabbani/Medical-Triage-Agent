from unittest.mock import Mock

from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.llm_risk_assessment import (
    LLMRiskAssessment,
)
from application.services.llm_service import LLMService
from workflow.triage_graph import build_triage_graph


def test_conversation_to_triage_flow():

    mock_llm_service = Mock(
        spec=LLMService
    )

    extraction_result = ConversationExtraction(
        intent="TRIAGE",
        symptoms=[
            "chest pain",
            "shortness of breath",
        ],
        severity="severe",
        age=None,
        duration="20 minutes",
        red_flags=[],
    )

    risk_result = LLMRiskAssessment(
        risk_level="HIGH",
        confidence=0.95,
        red_flags=[
            "chest pain with shortness of breath"
        ],
        recommendation=(
            "Emergency evaluation is required."
        ),
    )

    mock_llm_service.generate_structured.side_effect = [
        extraction_result,
        risk_result,
    ]

    graph = build_triage_graph(
        llm_service=mock_llm_service
    )

    state = {
        "patient_id": 2,
        "session_id": None,
        "user_message": (
            "I have severe chest pain and "
            "shortness of breath for 20 minutes."
        ),
        "age": None,
        "symptoms": [],
        "severity": None,
        "duration": None,
        "red_flags": [],
        "missing_information": [],
        "next_question": None,
        "conversation_history": [],
    }

    result = graph.invoke(state)

    assert result["intent"] == "TRIAGE"

    assert "chest pain" in result["symptoms"]

    assert (
        "shortness of breath"
        in result["symptoms"]
    )

    assert result["severity"] == "severe"

    assert result["duration"] == "20 minutes"

    assert result["risk_level"] == "HIGH"

    assert result["llm_risk_level"] == "HIGH"

    assert (
        mock_llm_service
        .generate_structured
        .call_count
        == 2
    )