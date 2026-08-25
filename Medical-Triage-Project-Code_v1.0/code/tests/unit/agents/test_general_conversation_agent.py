from application.agents.general_conversation_agent import (
    general_conversation_agent,
)


class FakeLLMService:

    def __init__(self, response):
        self.response = response

    def generate(
        self,
        prompt,
        system_prompt,
    ):
        return self.response


def test_general_conversation_returns_llm_response():

    llm = FakeLLMService(
        "سلام، خوشحالم که اینجا هستید."
    )

    state = {
        "user_message": "سلام",
        "user_roles": ["patient"],
        "patient_id": 1,
    }

    result = general_conversation_agent(
        state,
        llm_service=llm,
    )

    assert result["assistant_response"] == (
        "سلام، خوشحالم که اینجا هستید."
    )

    assert result["response"] == (
        "سلام، خوشحالم که اینجا هستید."
    )


def test_general_conversation_preserves_state():

    llm = FakeLLMService(
        "سلام"
    )

    state = {
        "user_message": "سلام",
        "user_roles": ["patient"],
        "patient_id": 10,
        "age": 30,
        "symptoms": ["headache"],
    }

    result = general_conversation_agent(
        state,
        llm_service=llm,
    )

    assert result["patient_id"] == 10
    assert result["age"] == 30
    assert result["symptoms"] == ["headache"]


def test_general_conversation_without_llm_has_fallback():

    state = {
        "user_message": "سلام",
        "user_roles": ["patient"],
        "patient_id": 1,
    }

    result = general_conversation_agent(
        state,
        llm_service=None,
    )

    assert result["assistant_response"]