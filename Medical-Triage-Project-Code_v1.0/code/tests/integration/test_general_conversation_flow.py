from unittest.mock import Mock

from application.contracts.conversation_intent import (
    ConversationIntent,
)
from application.contracts.general_conversation_response import (
    GeneralConversationResponse,
)
from application.services.llm_service import LLMService

from workflow.triage_graph import build_triage_graph


def test_general_conversation_flow():

    # =========================================================
    # Fake LLM
    # =========================================================

    mock_llm_service = Mock(spec=LLMService)

    intent_result = ConversationIntent(
        intent="GENERAL",
        confidence=0.99,
    )

    response_result = GeneralConversationResponse(
        response="Hello. How can I help you?"
    )

    mock_llm_service.generate_structured.side_effect = [
        intent_result,
        response_result,
    ]

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
    }

    # =========================================================
    # Execute
    # =========================================================

    result = graph.invoke(state)

    # =========================================================
    # Intent
    # =========================================================

    assert result["intent"] == "GENERAL"

    assert result["intent_confidence"] == 0.99

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

    assert "risk_level" not in result

    assert "llm_risk_level" not in result

    # =========================================================
    # LLM calls
    # =========================================================

    assert (
        mock_llm_service
        .generate_structured
        .call_count
        == 2
    )