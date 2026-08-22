from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.short_term_memory import (
    ShortTermMemory,
)
from application.services.short_term_memory_service import (
    ShortTermMemoryService,
)


def test_new_severity_replaces_old_severity():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            severity="moderate",
        ),
    )

    updated_memory = service.update(
        memory=memory,
        extraction=ConversationExtraction(
            severity="severe",
        ),
    )

    assert updated_memory.medical_context.severity == "severe"


def test_new_age_replaces_old_age():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            age=35,
        ),
    )

    updated_memory = service.update(
        memory=memory,
        extraction=ConversationExtraction(
            age=40,
        ),
    )

    assert updated_memory.medical_context.age == 40


def test_new_duration_replaces_old_duration():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            duration="2 hours",
        ),
    )

    updated_memory = service.update(
        memory=memory,
        extraction=ConversationExtraction(
            duration="5 hours",
        ),
    )

    assert updated_memory.medical_context.duration == "5 hours"


def test_none_does_not_replace_existing_value():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            age=35,
            severity="moderate",
            duration="2 hours",
        ),
    )

    updated_memory = service.update(
        memory=memory,
        extraction=ConversationExtraction(
            age=None,
            severity=None,
            duration=None,
        ),
    )

    assert updated_memory.medical_context.age == 35
    assert updated_memory.medical_context.severity == "moderate"
    assert updated_memory.medical_context.duration == "2 hours"


def test_symptoms_are_merged_not_replaced():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            symptoms=["chest pain"],
        ),
    )

    updated_memory = service.update(
        memory=memory,
        extraction=ConversationExtraction(
            symptoms=["headache"],
        ),
    )

    assert updated_memory.medical_context.symptoms == [
        "chest pain",
        "headache",
    ]


def test_red_flags_are_merged_not_replaced():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            red_flags=["chest pain"],
        ),
    )

    updated_memory = service.update(
        memory=memory,
        extraction=ConversationExtraction(
            red_flags=["difficulty breathing"],
        ),
    )

    assert updated_memory.medical_context.red_flags == [
        "chest pain",
        "difficulty breathing",
    ]


def test_same_scalar_value_is_idempotent():
    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=10,
        medical_context=ConversationExtraction(
            age=35,
            severity="severe",
            duration="2 hours",
        ),
    )

    updated_memory = service.update(
        memory=memory,
        extraction=ConversationExtraction(
            age=35,
            severity="severe",
            duration="2 hours",
        ),
    )

    assert updated_memory.medical_context.age == 35
    assert updated_memory.medical_context.severity == "severe"
    assert updated_memory.medical_context.duration == "2 hours"