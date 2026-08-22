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
    history = [
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

    service = ShortTermMemoryService()

    memory = service.load(
        session_id=10,
        history=history,
    )

    assert memory.session_id == 10
    assert memory.recent_messages == history

    assert memory.medical_context.symptoms == []
    assert memory.medical_context.red_flags == []
    assert memory.medical_context.age is None
    assert memory.medical_context.severity is None
    assert memory.medical_context.duration is None
    assert memory.intent is None


def test_update_short_term_memory():
    service = ShortTermMemoryService()

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


def test_update_does_not_duplicate_existing_symptoms():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            symptoms=["chest pain"],
        ),
    )

    extraction = ConversationExtraction(
        symptoms=[
            "chest pain",
            "shortness of breath",
        ],
    )

    updated_memory = service.update(
        memory=memory,
        extraction=extraction,
    )

    assert updated_memory.medical_context.symptoms == [
        "chest pain",
        "shortness of breath",
    ]


def test_update_does_not_duplicate_existing_red_flags():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            red_flags=["difficulty breathing"],
        ),
    )

    extraction = ConversationExtraction(
        red_flags=[
            "difficulty breathing",
            "cyanosis",
        ],
    )

    updated_memory = service.update(
        memory=memory,
        extraction=extraction,
    )

    assert updated_memory.medical_context.red_flags == [
        "difficulty breathing",
        "cyanosis",
    ]


def test_update_preserves_existing_values_when_new_values_are_none():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            symptoms=["chest pain"],
            age=35,
            severity="moderate",
            duration="2 hours",
        ),
    )

    extraction = ConversationExtraction(
        symptoms=[],
        age=None,
        severity=None,
        duration=None,
        red_flags=[],
    )

    updated_memory = service.update(
        memory=memory,
        extraction=extraction,
    )

    assert updated_memory.medical_context.symptoms == [
        "chest pain"
    ]

    assert updated_memory.medical_context.age == 35
    assert updated_memory.medical_context.severity == "moderate"
    assert updated_memory.medical_context.duration == "2 hours"


def test_update_replaces_existing_scalar_values():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            age=35,
            severity="moderate",
            duration="2 hours",
        ),
    )

    extraction = ConversationExtraction(
        age=40,
        severity="severe",
        duration="5 hours",
    )

    updated_memory = service.update(
        memory=memory,
        extraction=extraction,
    )

    assert updated_memory.medical_context.age == 40
    assert updated_memory.medical_context.severity == "severe"
    assert updated_memory.medical_context.duration == "5 hours"


def test_update_preserves_session_id():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=25,
        medical_context=ConversationExtraction(
            symptoms=["fever"],
        ),
    )

    extraction = ConversationExtraction(
        symptoms=["cough"],
    )

    updated_memory = service.update(
        memory=memory,
        extraction=extraction,
    )

    assert updated_memory.session_id == 25


def test_update_preserves_recent_messages():
    service = ShortTermMemoryService()

    history = [
        {
            "message_id": 1,
            "sender_type": "Patient",
            "content": "I have chest pain",
            "timestamp": None,
        },
    ]

    memory = ShortTermMemory(
        session_id=10,
        recent_messages=history,
        medical_context=ConversationExtraction(),
    )

    extraction = ConversationExtraction(
        symptoms=["chest pain"],
    )

    updated_memory = service.update(
        memory=memory,
        extraction=extraction,
    )

    assert updated_memory.recent_messages == history


def test_multiple_updates_remain_consistent():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
    )

    extraction_1 = ConversationExtraction(
        symptoms=["chest pain"],
        age=35,
    )

    memory = service.update(
        memory=memory,
        extraction=extraction_1,
    )

    extraction_2 = ConversationExtraction(
        symptoms=["shortness of breath"],
        severity="severe",
    )

    memory = service.update(
        memory=memory,
        extraction=extraction_2,
    )

    extraction_3 = ConversationExtraction(
        duration="30 minutes",
        red_flags=["difficulty breathing"],
    )

    memory = service.update(
        memory=memory,
        extraction=extraction_3,
    )

    assert memory.session_id == 10

    assert memory.medical_context.symptoms == [
        "chest pain",
        "shortness of breath",
    ]

    assert memory.medical_context.age == 35
    assert memory.medical_context.severity == "severe"
    assert memory.medical_context.duration == "30 minutes"

    assert memory.medical_context.red_flags == [
        "difficulty breathing"
    ]