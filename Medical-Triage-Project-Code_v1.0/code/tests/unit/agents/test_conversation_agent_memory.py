from agents.conversation_agent import (
    conversation_agent,
)
from application.contracts.conversation_extraction import (
    ConversationExtraction,
)


class FakeLLMService:

    def __init__(self, responses):
        self.responses = iter(responses)

    def generate_structured(
        self,
        prompt,
        response_model,
        system_prompt,
    ):
        return next(self.responses)


def test_multi_turn_information_is_preserved():

    llm = FakeLLMService(
        [
            ConversationExtraction(
                symptoms=["headache"]
            ),
            ConversationExtraction(
                age=30
            ),
            ConversationExtraction(
                duration="2 days"
            ),
            ConversationExtraction(
                severity="moderate"
            ),
        ]
    )

    state = {
        "session_id": 1,
        "user_message": "سرم درد می‌کنه",
        "symptoms": [],
        "age": None,
        "duration": None,
        "severity": None,
        "red_flags": [],
        "missing_information": [],
        "next_question": None,
        "conversation_history": [],
        "short_term_memory": None,
        "intent": None,
    }

    # Turn 1
    state = conversation_agent(
        state,
        llm_service=llm,
    )

    assert state["symptoms"] == ["headache"]

    # Turn 2
    state["user_message"] = "۳۰ سالمه"

    state = conversation_agent(
        state,
        llm_service=llm,
    )

    assert state["symptoms"] == ["headache"]
    assert state["age"] == 30

    # Turn 3
    state["user_message"] = "دو روزه"

    state = conversation_agent(
        state,
        llm_service=llm,
    )

    assert state["symptoms"] == ["headache"]
    assert state["age"] == 30
    assert state["duration"] == "2 days"

    # Turn 4
    state["user_message"] = "متوسطه"

    state = conversation_agent(
        state,
        llm_service=llm,
    )

    assert state["symptoms"] == ["headache"]
    assert state["age"] == 30
    assert state["duration"] == "2 days"
    assert state["severity"] == "moderate"