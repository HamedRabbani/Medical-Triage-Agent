from unittest.mock import Mock

from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.short_term_memory import (
    ShortTermMemory,
)
from agents.conversation_agent import conversation_agent


def build_llm(extraction: ConversationExtraction) -> Mock:
    llm = Mock()

    llm.generate_structured.return_value = extraction

    return llm


def test_conversation_agent_updates_short_term_memory():
    llm = build_llm(
        ConversationExtraction(
            symptoms=["chest pain"],
            age=35,
            severity="moderate",
            duration=None,
            red_flags=[],
        )
    )

    state = {
        "session_id": 10,
        "user_message": "I have chest pain.",
        "conversation_history": [],
        "short_term_memory": ShortTermMemory(
            session_id=10,
        ),
        "intent": None,
        "missing_information": [],
        "next_question": None,
        "symptoms": [],
        "age": None,
        "severity": None,
        "duration": None,
        "red_flags": [],
    }

    result = conversation_agent(
        state,
        llm_service=llm,
    )

    memory = result["short_term_memory"]

    assert memory.session_id == 10

    assert memory.medical_context.symptoms == [
        "chest pain"
    ]

    assert memory.medical_context.age == 35
    assert memory.medical_context.severity == "moderate"

    assert result["symptoms"] == [
        "chest pain"
    ]

    assert result["age"] == 35
    assert result["severity"] == "moderate"


def test_conversation_agent_preserves_memory_across_turns():
    llm = Mock()

    state = {
        "session_id": 10,
        "user_message": "It started 30 minutes ago.",
        "conversation_history": [
            {
                "message_id": 1,
                "sender_type": "Patient",
                "content": "I have chest pain.",
                "timestamp": None,
            }
        ],
        "short_term_memory": ShortTermMemory(
            session_id=10,
            recent_messages=[
                {
                    "message_id": 1,
                    "sender_type": "Patient",
                    "content": "I have chest pain.",
                    "timestamp": None,
                }
            ],
            medical_context=ConversationExtraction(
                symptoms=["chest pain"],
                age=35,
                severity="moderate",
            ),
        ),
        "intent": "TRIAGE",
        "missing_information": ["duration"],
        "next_question": "How long has it been happening?",
        "symptoms": ["chest pain"],
        "age": 35,
        "severity": "moderate",
        "duration": None,
        "red_flags": [],
    }

    llm.generate_structured.return_value = (
        ConversationExtraction(
            symptoms=[],
            age=None,
            severity=None,
            duration="30 minutes",
            red_flags=[],
        )
    )

    result = conversation_agent(
        state,
        llm_service=llm,
    )

    memory = result["short_term_memory"]

    assert memory.session_id == 10

    assert memory.medical_context.symptoms == [
        "chest pain"
    ]

    assert memory.medical_context.age == 35

    assert memory.medical_context.severity == "moderate"

    assert memory.medical_context.duration == "30 minutes"

    assert result["symptoms"] == [
        "chest pain"
    ]

    assert result["age"] == 35

    assert result["severity"] == "moderate"

    assert result["duration"] == "30 minutes"


def test_conversation_agent_accumulates_memory_across_multiple_turns():
    llm = Mock()

    state = {
        "session_id": 10,
        "user_message": "The pain is severe.",
        "conversation_history": [],
        "short_term_memory": ShortTermMemory(
            session_id=10,
            medical_context=ConversationExtraction(
                symptoms=["chest pain"],
                age=35,
            ),
        ),
        "intent": "TRIAGE",
        "missing_information": ["severity"],
        "next_question": "How severe is the pain?",
        "symptoms": ["chest pain"],
        "age": 35,
        "severity": None,
        "duration": None,
        "red_flags": [],
    }

    llm.generate_structured.return_value = (
        ConversationExtraction(
            symptoms=["shortness of breath"],
            age=None,
            severity="severe",
            duration=None,
            red_flags=["difficulty breathing"],
        )
    )

    result = conversation_agent(
        state,
        llm_service=llm,
    )

    memory = result["short_term_memory"]

    assert memory.medical_context.symptoms == [
        "chest pain",
        "shortness of breath",
    ]

    assert memory.medical_context.age == 35

    assert memory.medical_context.severity == "severe"

    assert memory.medical_context.red_flags == [
        "difficulty breathing"
    ]

    assert result["symptoms"] == [
        "chest pain",
        "shortness of breath",
    ]

    assert result["age"] == 35

    assert result["severity"] == "severe"

    assert result["red_flags"] == [
        "difficulty breathing"
    ]


def test_conversation_agent_does_not_duplicate_memory():
    llm = build_llm(
        ConversationExtraction(
            symptoms=[
                "chest pain",
                "shortness of breath",
            ],
            age=None,
            severity="severe",
            duration=None,
            red_flags=[
                "difficulty breathing"
            ],
        )
    )

    state = {
        "session_id": 10,
        "user_message": "I still have chest pain.",
        "conversation_history": [],
        "short_term_memory": ShortTermMemory(
            session_id=10,
            medical_context=ConversationExtraction(
                symptoms=[
                    "chest pain",
                    "shortness of breath",
                ],
                age=35,
                severity="moderate",
                red_flags=[
                    "difficulty breathing"
                ],
            ),
        ),
        "intent": "TRIAGE",
        "missing_information": [],
        "next_question": None,
        "symptoms": [
            "chest pain",
            "shortness of breath",
        ],
        "age": 35,
        "severity": "moderate",
        "duration": None,
        "red_flags": [
            "difficulty breathing"
        ],
    }

    result = conversation_agent(
        state,
        llm_service=llm,
    )

    memory = result["short_term_memory"]

    assert memory.medical_context.symptoms == [
        "chest pain",
        "shortness of breath",
    ]

    assert memory.medical_context.red_flags == [
        "difficulty breathing"
    ]

    assert memory.medical_context.age == 35
    assert memory.medical_context.severity == "severe"