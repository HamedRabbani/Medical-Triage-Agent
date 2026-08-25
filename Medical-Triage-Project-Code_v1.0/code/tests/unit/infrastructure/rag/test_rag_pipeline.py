from application.services.rag_service import RAGService
from infrastructure.rag.rag_pipeline import RAGPipeline


class FakeDocumentLoader:

    def __init__(self, documents):

        self.documents = documents

    def load(self):

        return self.documents


class FakeChunker:

    def chunk(self, documents):

        return [
            {
                "id": "chunk-1",
                "source": "medical.txt",
                "content": "Headache information",
                "metadata": {},
            }
        ]


class FakeRAGRepository:

    def __init__(self):

        self.documents = None

    def add_documents(self, documents):

        self.documents = documents

    def retrieve(
        self,
        query,
        top_k=5,
        distance_threshold=None,
    ):

        return [
            {
                "content": "Headache information",
                "source": "medical.txt",
                "distance": 0.1,
            }
        ]


def test_pipeline_ingest():

    documents = [
        {
            "source": "medical.txt",
            "content": "Headache information",
        }
    ]

    repository = FakeRAGRepository()

    service = RAGService(
        rag_repository=repository
    )

    pipeline = RAGPipeline(
        rag_service=service,
        document_loader=FakeDocumentLoader(
            documents
        ),
        chunker=FakeChunker(),
    )

    count = pipeline.ingest()

    assert count == 1

    assert repository.documents == [
        {
            "id": "chunk-1",
            "source": "medical.txt",
            "content": "Headache information",
            "metadata": {},
        }
    ]


def test_pipeline_ingest_empty_documents():

    repository = FakeRAGRepository()

    service = RAGService(
        rag_repository=repository
    )

    pipeline = RAGPipeline(
        rag_service=service,
        document_loader=FakeDocumentLoader([]),
        chunker=FakeChunker(),
    )

    count = pipeline.ingest()

    assert count == 0
    assert repository.documents is None