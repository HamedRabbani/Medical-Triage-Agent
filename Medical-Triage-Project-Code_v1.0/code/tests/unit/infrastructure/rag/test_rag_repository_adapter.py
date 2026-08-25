from infrastructure.rag.rag_repository_adapter import (
    RAGRepositoryAdapter,
)


class FakeEmbeddingService:

    def embed_documents(
        self,
        texts,
    ):

        return [
            [1.0, 0.0],
            [0.0, 1.0],
        ]

    def embed_query(
        self,
        text,
    ):

        return [1.0, 0.0]


class FakeVectorStore:

    def __init__(self):

        self.documents = None
        self.embeddings = None
        self.search_embedding = None
        self.search_top_k = None

    def add_documents(
        self,
        documents,
        embeddings,
    ):

        self.documents = documents
        self.embeddings = embeddings

    def similarity_search(
        self,
        query_embedding,
        top_k,
    ):

        self.search_embedding = query_embedding
        self.search_top_k = top_k

        return [
            {
                "content": "Headache information",
                "source": "medical.txt",
                "distance": 0.1,
            }
        ]


def test_add_documents():

    embedding_service = FakeEmbeddingService()
    vector_store = FakeVectorStore()

    adapter = RAGRepositoryAdapter(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    documents = [
        {
            "id": "doc-1",
            "source": "medical.txt",
            "content": "Headache information",
        },
        {
            "id": "doc-2",
            "source": "medical.txt",
            "content": "Fever information",
        },
    ]

    adapter.add_documents(documents)

    assert vector_store.documents == documents

    assert vector_store.embeddings == [
        [1.0, 0.0],
        [0.0, 1.0],
    ]


def test_retrieve():

    embedding_service = FakeEmbeddingService()
    vector_store = FakeVectorStore()

    adapter = RAGRepositoryAdapter(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    results = adapter.retrieve(
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

    assert vector_store.search_embedding == [
        1.0,
        0.0,
    ]

    assert vector_store.search_top_k == 3


def test_retrieve_empty_query():

    adapter = RAGRepositoryAdapter(
        embedding_service=FakeEmbeddingService(),
        vector_store=FakeVectorStore(),
    )

    results = adapter.retrieve(
        query="   ",
    )

    assert results == []


def test_add_empty_documents():

    vector_store = FakeVectorStore()

    adapter = RAGRepositoryAdapter(
        embedding_service=FakeEmbeddingService(),
        vector_store=vector_store,
    )

    adapter.add_documents([])

    assert vector_store.documents is None