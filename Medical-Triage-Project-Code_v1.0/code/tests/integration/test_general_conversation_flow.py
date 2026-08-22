from unittest.mock import Mock

from application.services.llm_service import LLMService
from workflow.triage_graph import build_triage_graph


def test_general_conversation_flow():

    # =========================================================
    # Fake LLM
    # =========================================================

    mock_llm_service = Mock(
        spec=LLMService
    )

    # Current architecture:
    # Intent detection is deterministic.
    # General conversation uses plain-text generation.

    mock_llm_service.generate.return_value = (
        "Hello. How can I help you?"
    )

    # =========================================================
    # Build Graph
    # =========================================================

    graph = build_triage_graph(
        llm_service=mock_llm_service,
    )

    # =========================================================
    # State
    # =========================================================

    state = {
        "patient_id": 2,
        "session_id": None,

        "user_message": "Hello, how are you?",

        "intent": None,
        "intent_confidence": None,

        "age": None,
        "symptoms": [],
        "severity": None,
        "duration": None,

        "red_flags": [],
        "missing_information": [],
        "next_question": None,

        "conversation_history": [],
    }

    # =========================================================
    # Execute
    # =========================================================

    result = graph.invoke(
        state
    )

    # =========================================================
    # Intent
    # =========================================================

    assert result["intent"] == "GENERAL"

    assert (
        result["intent_confidence"]
        == 0.9
    )

    # =========================================================
    # Response
    # =========================================================

    assert (
        result["assistant_response"]
        == "Hello. How can I help you?"
    )

    # =========================================================
    # Triage must NOT execute
    # =========================================================

    assert result.get(
        "risk_level"
    ) is None

    assert result.get(
        "llm_risk_level"
    ) is None

    # =========================================================
    # LLM Calls
    # =========================================================

    assert (
        mock_llm_service.generate.call_count
        == 1
    )

    assert (
        mock_llm_service
        .generate_structured
        .call_count
        == 0
    )