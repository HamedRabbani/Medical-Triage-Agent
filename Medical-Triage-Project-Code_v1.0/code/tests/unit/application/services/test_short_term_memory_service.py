from unittest.mock import Mock

from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.short_term_memory import (
    ShortTermMemory,
)
from application.services.short_term_memory_service import (
    ShortTermMemoryService,
)


def test_load_short_term_memory():
    conversation_service = Mock()

    conversation_service.get_history.return_value = [
        {
            "message_id": 1,
            "sender_type": "Patient",
            "content": "I have chest pain",
            "timestamp": None,
        },
        {
            "message_id": 2,
            "sender_type": "Patient",
            "content": "It started this morning",
            "timestamp": None,
        },
    ]

    service = ShortTermMemoryService(
        conversation_service
    )

    memory = service.load(session_id=10)

    assert memory.session_id == 10

    assert memory.recent_messages == [
        {
            "message_id": 1,
            "sender_type": "Patient",
            "content": "I have chest pain",
            "timestamp": None,
        },
        {
            "message_id": 2,
            "sender_type": "Patient",
            "content": "It started this morning",
            "timestamp": None,
        },
    ]

    conversation_service.get_history.assert_called_once_with(
        10
    )


def test_update_short_term_memory():
    conversation_service = Mock()

    service = ShortTermMemoryService(
        conversation_service
    )

    memory = ShortTermMemory(
        session_id=10,
        recent_messages=[],
        medical_context=ConversationExtraction(
            symptoms=["chest pain"],
            age=35,
            severity="moderate",
        ),
    )

    extraction = ConversationExtraction(
        symptoms=["shortness of breath"],
        age=None,
        severity="severe",
        duration="2 hours",
        red_flags=["difficulty breathing"],
    )

    updated_memory = service.update(
        memory=memory,
        extraction=extraction,
    )

    assert updated_memory.session_id == 10

    assert updated_memory.medical_context.symptoms == [
        "chest pain",
        "shortness of breath",
    ]

    assert updated_memory.medical_context.age == 35

    assert updated_memory.medical_context.severity == "severe"

    assert updated_memory.medical_context.duration == "2 hours"

    assert updated_memory.medical_context.red_flags == [
        "difficulty breathing"
    ]