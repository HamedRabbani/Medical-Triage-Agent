from agents.conversation_agent import conversation_agent


def test_general_greeting():

    state = {
        "user_message": "سلام خوبی؟",
        "intent": None,
        "symptoms": [],
        "age": None,
        "duration": None,
        "severity": None,
        "missing_information": [],
        "next_question": None,
        "risk_level": None,
    }

    result = conversation_agent(state)

    assert result["intent"] == "GENERAL"


def test_general_help_request():

    state = {
        "user_message": "میتونی کمکم کنی؟",
        "intent": None,
        "symptoms": [],
        "age": None,
        "duration": None,
        "severity": None,
        "missing_information": [],
        "next_question": None,
        "risk_level": None,
    }

    result = conversation_agent(state)

    assert result["intent"] == "GENERAL"


def test_chest_pain_is_triage():

    state = {
        "user_message": "درد قفسه سینه دارم",
        "intent": None,
        "symptoms": [],
        "age": None,
        "duration": None,
        "severity": None,
        "missing_information": [],
        "next_question": None,
        "risk_level": None,
    }

    result = conversation_agent(state)

    assert result["intent"] == "TRIAGE"


def test_shortness_of_breath_is_triage():

    state = {
        "user_message": "نفس تنگی دارم",
        "intent": None,
        "symptoms": [],
        "age": None,
        "duration": None,
        "severity": None,
        "missing_information": [],
        "next_question": None,
        "risk_level": None,
    }

    result = conversation_agent(state)

    assert result["intent"] == "TRIAGE"


def test_triage_followup_stays_triage():

    state = {
        "user_message": "29",
        "intent": "TRIAGE",
        "symptoms": ["chest pain"],
        "age": None,
        "duration": None,
        "severity": None,
        "missing_information": ["age"],
        "next_question": "چند سال دارید؟",
        "risk_level": None,
    }

    result = conversation_agent(state)

    assert result["intent"] == "TRIAGE"