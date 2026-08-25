from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.short_term_memory import (
    ShortTermMemory,
)
from application.services.short_term_memory_service import (
    ShortTermMemoryService,
)


def test_memory_preserves_previous_medical_information():

    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=1,
        medical_context=ConversationExtraction(
            symptoms=["headache"],
            age=30,
            duration="2 days",
        ),
    )

    extraction = ConversationExtraction(
        severity="severe"
    )

    updated = service.update(
        memory,
        extraction,
    )

    assert updated.medical_context.age == 30
    assert updated.medical_context.duration == "2 days"
    assert updated.medical_context.symptoms == ["headache"]
    assert updated.medical_context.severity == "severe"


def test_memory_merges_new_symptoms():

    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=1,
        medical_context=ConversationExtraction(
            symptoms=["headache"]
        ),
    )

    extraction = ConversationExtraction(
        symptoms=["fever"]
    )

    updated = service.update(
        memory,
        extraction,
    )

    assert updated.medical_context.symptoms == [
        "headache",
        "fever",
    ]


def test_memory_does_not_duplicate_symptoms():

    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=1,
        medical_context=ConversationExtraction(
            symptoms=["headache"]
        ),
    )

    extraction = ConversationExtraction(
        symptoms=["headache"]
    )

    updated = service.update(
        memory,
        extraction,
    )

    assert updated.medical_context.symptoms == [
        "headache"
    ]


def test_memory_preserves_previous_severity():

    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=1,
        medical_context=ConversationExtraction(
            severity="moderate"
        ),
    )

    extraction = ConversationExtraction()

    updated = service.update(
        memory,
        extraction,
    )

    assert (
        updated.medical_context.severity
        == "moderate"
    )


def test_memory_preserves_previous_age():

    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=1,
        medical_context=ConversationExtraction(
            age=42
        ),
    )

    extraction = ConversationExtraction()

    updated = service.update(
        memory,
        extraction,
    )

    assert updated.medical_context.age == 42


def test_memory_preserves_previous_duration():

    service = ShortTermMemoryService()

    memory = ShortTermMemory(
        session_id=1,
        medical_context=ConversationExtraction(
            duration="3 days"
        ),
    )

    extraction = ConversationExtraction()

    updated = service.update(
        memory,
        extraction,
    )

    assert (
        updated.medical_context.duration
        == "3 days"
    )