from agents.rag_agent import rag_agent


class FakeRAGService:

    def __init__(self):
        self.query = None
        self.top_k = None
        self.distance_threshold = None

    def retrieve(
        self,
        query,
        top_k=5,
        distance_threshold=None,
    ):
        self.query = query
        self.top_k = top_k
        self.distance_threshold = distance_threshold

        return [
            {
                "content": "Headache medical information",
                "source": "headache.txt",
                "distance": 0.1,
            }
        ]


def test_rag_agent_retrieves_context():

    rag_service = FakeRAGService()

    state = {
        "symptoms": ["headache"],
        "age": 29,
        "duration": "one week",
        "severity": "severe",
        "red_flags": [],
    }

    result = rag_agent(
        state,
        rag_service,
    )

    assert len(result["rag_context"]) == 1

    assert (
        result["rag_context"][0]["content"]
        == "Headache medical information"
    )

    assert rag_service.top_k == 3

    assert rag_service.distance_threshold == 20

    assert "headache" in (
        rag_service.query.lower()
    )


def test_rag_agent_returns_empty_context_without_data():

    rag_service = FakeRAGService()

    state = {
        "symptoms": [],
        "age": None,
        "duration": None,
        "severity": None,
        "red_flags": [],
    }

    result = rag_agent(
        state,
        rag_service,
    )

    assert result["rag_context"] == []

    assert rag_service.query is None

    assert rag_service.distance_threshold is None