from unittest.mock import Mock

from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.conversation_intent import (
    ConversationIntent,
)
from application.contracts.general_conversation_response import (
    GeneralConversationResponse,
)
from agents.conversation_agent import conversation_agent


def test_triage_intent_extracts_medical_information():

    state = {
        "user_message": (
            "I have severe chest pain "
            "and shortness of breath."
        ),
        "symptoms": [],
        "severity": None,
        "age": None,
        "duration": None,
        "red_flags": [],
    }

    mock_llm = Mock()

    mock_llm.generate_structured.side_effect = [

        ConversationIntent(
            intent="TRIAGE",
            confidence=0.99,
        ),

        ConversationExtraction(
            intent="TRIAGE",
            symptoms=[
                "chest pain",
                "shortness of breath",
            ],
            severity="severe",
            age=None,
            duration=None,
            red_flags=[],
        ),
    ]

    result = conversation_agent(
        state,
        llm_service=mock_llm,
    )

    assert result["intent"] == "TRIAGE"

    assert result["intent_confidence"] == 0.99

    assert "chest pain" in result["symptoms"]

    assert (
        "shortness of breath"
        in result["symptoms"]
    )

    assert result["severity"] == "severe"

    assert (
        mock_llm.generate_structured.call_count
        == 2
    )


def test_general_intent_generates_general_response():

    state = {
        "user_message": "سلام، حالت چطوره؟",
        "symptoms": [],
        "severity": None,
        "age": None,
        "duration": None,
        "red_flags": [],
    }

    mock_llm = Mock()

    mock_llm.generate_structured.side_effect = [

        ConversationIntent(
            intent="GENERAL",
            confidence=0.99,
        ),

        GeneralConversationResponse(
            response="Hello. How can I help you?"
        ),
    ]

    result = conversation_agent(
        state,
        llm_service=mock_llm,
    )

    assert result["intent"] == "GENERAL"

    assert result["intent_confidence"] == 0.99

    assert (
        result["assistant_response"]
        == "Hello. How can I help you?"
    )

    assert result["symptoms"] == []

    assert (
        mock_llm.generate_structured.call_count
        == 2
    )