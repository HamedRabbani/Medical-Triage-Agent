from agents.symptom_agent import symptom_agent


class FakeLLMService:

    def extract_symptoms(self, text):
        from application.contracts.llm_test_response import (
            LLMTestResponse,
        )

        return LLMTestResponse(
            symptoms=["fever", "headache"],
            confidence=0.95,
        )


def test_symptom_agent_with_llm():

    state = {
        "user_message": "من تب و سردرد دارم",
        "conversation_history": [],
        "symptoms": [],
        "age": None,
        "duration": None,
        "severity": None,
    }

    result = symptom_agent(
        state,
        llm_service=FakeLLMService(),
    )

    assert "fever" in result["symptoms"]
    assert "headache" in result["symptoms"]