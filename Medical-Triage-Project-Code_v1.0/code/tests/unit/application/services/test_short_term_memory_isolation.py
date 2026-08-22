from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.short_term_memory import (
    ShortTermMemory,
)
from application.services.short_term_memory_service import (
    ShortTermMemoryService,
)


def test_memory_isolated_by_session_id():
    service = ShortTermMemoryService()

    memory_session_1 = ShortTermMemory(
        session_id=1,
        medical_context=ConversationExtraction(
            symptoms=["chest pain"],
            age=35,
        ),
    )

    memory_session_2 = ShortTermMemory(
        session_id=2,
        medical_context=ConversationExtraction(
            symptoms=["headache"],
            age=40,
        ),
    )

    updated_session_1 = service.update(
        memory=memory_session_1,
        extraction=ConversationExtraction(
            symptoms=["shortness of breath"],
        ),
    )

    updated_session_2 = service.update(
        memory=memory_session_2,
        extraction=ConversationExtraction(
            symptoms=["fever"],
        ),
    )

    assert updated_session_1.session_id == 1
    assert updated_session_2.session_id == 2

    assert updated_session_1.medical_context.symptoms == [
        "chest pain",
        "shortness of breath",
    ]

    assert updated_session_2.medical_context.symptoms == [
        "headache",
        "fever",
    ]

    assert "headache" not in (
        updated_session_1.medical_context.symptoms
    )

    assert "chest pain" not in (
        updated_session_2.medical_context.symptoms
    )


def test_memory_update_does_not_mutate_original_memory():
    service = ShortTermMemoryService()

    original_memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            symptoms=["chest pain"],
            age=35,
        ),
    )

    updated_memory = service.update(
        memory=original_memory,
        extraction=ConversationExtraction(
            symptoms=["fever"],
            severity="severe",
        ),
    )

    assert original_memory.session_id == 10

    assert original_memory.medical_context.symptoms == [
        "chest pain"
    ]

    assert original_memory.medical_context.age == 35

    assert original_memory.medical_context.severity is None

    assert updated_memory.medical_context.symptoms == [
        "chest pain",
        "fever",
    ]

    assert updated_memory.medical_context.age == 35
    assert updated_memory.medical_context.severity == "severe"


def test_load_memory_does_not_share_history_between_sessions():
    service = ShortTermMemoryService()

    history_session_1 = [
        {
            "message_id": 1,
            "sender_type": "Patient",
            "content": "I have chest pain.",
            "timestamp": None,
        }
    ]

    history_session_2 = [
        {
            "message_id": 2,
            "sender_type": "Patient",
            "content": "I have a headache.",
            "timestamp": None,
        }
    ]

    memory_session_1 = service.load(
        session_id=1,
        history=history_session_1,
    )

    memory_session_2 = service.load(
        session_id=2,
        history=history_session_2,
    )

    assert memory_session_1.session_id == 1
    assert memory_session_2.session_id == 2

    assert memory_session_1.recent_messages == (
        history_session_1
    )

    assert memory_session_2.recent_messages == (
        history_session_2
    )

    assert memory_session_1.recent_messages != (
        memory_session_2.recent_messages
    )

    assert (
        memory_session_1.recent_messages[0]["content"]
        == "I have chest pain."
    )

    assert (
        memory_session_2.recent_messages[0]["content"]
        == "I have a headache."
    )