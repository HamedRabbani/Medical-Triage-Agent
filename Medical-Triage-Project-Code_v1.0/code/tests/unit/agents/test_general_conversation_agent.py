from agents.conversation_agent import conversation_agent


def test_triage_intent_is_detected_from_medical_message():
    state = {
        "user_message": (
            "I have chest pain "
            "and shortness of breath."
        ),
        "symptoms": [],
        "severity": None,
        "age": None,
        "duration": None,
        "red_flags": [],
    }

    result = conversation_agent(state)

    assert result["intent"] == "TRIAGE"
    assert result["intent_confidence"] == 1.0
    assert result["assistant_response"] is None


def test_general_intent_is_detected():
    state = {
        "user_message": "سلام، حالت چطوره؟",
        "symptoms": [],
        "severity": None,
        "age": None,
        "duration": None,
        "red_flags": [],
    }

    result = conversation_agent(state)

    assert result["intent"] == "GENERAL"
    assert result["intent_confidence"] == 0.9
    assert result["assistant_response"] is None