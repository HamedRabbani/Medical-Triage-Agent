from workflow.triage_graph import route_intent


def test_general_intent_without_triage_context() -> None:
    state = {
        "intent": "GENERAL",
        "symptoms": [],
        "severity": None,
        "duration": None,
        "age": None,
        "red_flags": [],
        "missing_information": [],
        "session_id": None,
        "next_question": None,
        "risk_level": None,
        "recommendation": None,
    }

    assert route_intent(state) == "general"


def test_general_intent_during_active_triage() -> None:
    state = {
        "intent": "GENERAL",
        "symptoms": ["chest pain"],
        "severity": None,
        "duration": None,
        "age": 29,
        "red_flags": [],
        "missing_information": ["severity"],
        "session_id": 572,
        "next_question": "How severe are your symptoms?",
        "risk_level": None,
        "recommendation": None,
    }

    assert route_intent(state) == "triage"


def test_explicit_triage_intent() -> None:
    state = {
        "intent": "TRIAGE",
        "symptoms": [],
        "severity": None,
        "duration": None,
        "age": None,
        "red_flags": [],
        "missing_information": [],
        "session_id": None,
        "next_question": None,
        "risk_level": None,
        "recommendation": None,
    }

    assert route_intent(state) == "triage"