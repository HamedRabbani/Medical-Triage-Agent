from agents.risk_agent import risk_agent
from application.contracts.llm_risk_assessment import (
    LLMRiskAssessment,
)


class FakeLLMService:

    def __init__(self):
        self.prompt = None

    def generate_structured(
        self,
        prompt,
        response_model,
        system_prompt,
    ):
        self.prompt = prompt

        return LLMRiskAssessment(
            risk_level="LOW",
            confidence=0.80,
            red_flags=[],
            recommendation="Monitor symptoms.",
        )


class FakeRAGService:

    def __init__(self):
        self.query = None

    def retrieve(
        self,
        query,
        top_k=5,
    ):
        self.query = query

        return [
            {
                "source": "headache.txt",
                "content": (
                    "Persistent or worsening headaches "
                    "should be evaluated by a healthcare "
                    "professional."
                ),
                "distance": 0.2,
            }
        ]


def test_rag_context_reaches_risk_agent():

    rag_service = FakeRAGService()
    llm_service = FakeLLMService()

    query = "severe headache"

    rag_context = rag_service.retrieve(
        query=query,
        top_k=5,
    )

    state = {
        "symptoms": ["headache"],
        "severity": "severe",
        "age": 29,
        "duration": "one week",
        "red_flags": [],
        "rag_context": rag_context,
    }

    result = risk_agent(
        state,
        llm_service=llm_service,
    )

    # RAG was called
    assert rag_service.query == query

    # RAG result reached the Risk Agent
    assert result["rag_context"] == rag_context

    # RAG context reached the LLM
    assert (
        "Persistent or worsening headaches"
        in llm_service.prompt
    )