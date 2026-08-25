from application.services.rag_service import RAGService


class FakeRAGRepository:

    def __init__(self):
        self.documents = None
        self.query = None
        self.top_k = None
        self.distance_threshold = None

    def add_documents(self, documents):
        self.documents = documents

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
                "content": "Headache information",
                "source": "medical.txt",
                "distance": 0.1,
            }
        ]


def test_add_documents():

    repository = FakeRAGRepository()

    service = RAGService(
        rag_repository=repository
    )

    documents = [
        {
            "chunk_id": "doc-1",
            "source": "medical.txt",
            "content": "Headache information",
        }
    ]

    service.add_documents(documents)

    assert repository.documents == documents


def test_retrieve():

    repository = FakeRAGRepository()

    service = RAGService(
        rag_repository=repository
    )

    results = service.retrieve(
        query="headache",
        top_k=3,
    )

    assert results == [
        {
            "content": "Headache information",
            "source": "medical.txt",
            "distance": 0.1,
        }
    ]

    assert repository.query == "headache"
    assert repository.top_k == 3
    assert repository.distance_threshold is None