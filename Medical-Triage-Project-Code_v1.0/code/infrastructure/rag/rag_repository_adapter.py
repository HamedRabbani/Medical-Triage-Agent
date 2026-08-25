
from application.ports.rag_port import RAGPort

from infrastructure.rag.embedding_adapter import (
    EmbeddingAdapter,
)

from infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)


class RAGRepositoryAdapter(RAGPort):
    """
    Infrastructure implementation of RAGPort.

    Coordinates:
        EmbeddingAdapter
            ↓
        ChromaVectorStore
    """

    def __init__(
        self,
        embedding_service: EmbeddingAdapter,
        vector_store: ChromaVectorStore,
    ) -> None:
        self.embedding_service = (
            embedding_service
        )

        self.vector_store = vector_store

    def add_documents(
        self,
        documents: list[dict],
    ) -> None:

        if not documents:
            return

        texts = [
            str(
                document.get(
                    "content",
                    "",
                )
            )
            for document in documents
        ]

        embeddings = (
            self.embedding_service
            .embed_documents(texts)
        )

        self.vector_store.add_documents(
            documents=documents,
            embeddings=embeddings,
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        distance_threshold: float | None = None,
    ) -> list[dict]:

        if not query or not query.strip():
            return []

        query_embedding = (
            self.embedding_service
            .embed_query(query)
        )

        if not query_embedding:
            return []

        results = (
            self.vector_store
            .similarity_search(
                query_embedding=query_embedding,
                top_k=top_k,
            )
        )

        if distance_threshold is None:
            return results

        return [
            result
            for result in results
            if (
                result.get("distance")
                is not None
                and result["distance"]
                <= distance_threshold
            )
        ]

