from application.contracts.short_term_memory import ShortTermMemory


def test_short_term_memory_defaults():
    memory = ShortTermMemory(
        session_id=1
    )

    assert memory.session_id == 1
    assert memory.recent_messages == []

    assert memory.medical_context.symptoms == []
    assert memory.medical_context.red_flags == []
    assert memory.medical_context.age is None
    assert memory.medical_context.severity is None
    assert memory.medical_context.duration is None

    assert memory.intent is None


def test_short_term_memory_with_data():
    memory = ShortTermMemory(
        session_id=1,
        recent_messages=[
            {
                "message_id": 1,
                "sender_type": "Patient",
                "content": "I have chest pain",
                "timestamp": None,
            }
        ],
        medical_context={
            "symptoms": ["chest pain"],
            "severity": "severe",
            "age": 35,
            "duration": "2 hours",
            "red_flags": ["chest pain"],
        },
        intent="TRIAGE",
    )

    assert memory.session_id == 1

    assert memory.recent_messages[0]["content"] == (
        "I have chest pain"
    )

    assert memory.medical_context.symptoms == [
        "chest pain"
    ]

    assert memory.medical_context.severity == "severe"
    assert memory.medical_context.age == 35
    assert memory.medical_context.duration == "2 hours"

    assert memory.medical_context.red_flags == [
        "chest pain"
    ]

    assert memory.intent == "TRIAGE"