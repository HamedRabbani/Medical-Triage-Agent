from application.agents.intent_router import (
    ConversationIntent,
    intent_router,
)


def test_router_general_conversation():

    state = {
        "user_message": "Hello, how are you?"
    }

    result = intent_router(state)

    assert result["intent"] == ConversationIntent.GENERAL.value


def test_router_medical_triage():

    state = {
        "user_message": "I have chest pain."
    }

    result = intent_router(state)

    assert result["intent"] == ConversationIntent.TRIAGE.value


def test_router_persian_medical_message():

    state = {
        "user_message": "قفسه سینه‌ام درد می‌کند"
    }

    result = intent_router(state)

    assert result["intent"] == ConversationIntent.TRIAGE.value