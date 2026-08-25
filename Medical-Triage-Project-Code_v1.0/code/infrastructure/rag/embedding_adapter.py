
from typing import Any


class EmbeddingAdapter:
    """
    Infrastructure adapter around the configured embedding model.

    Keeps the concrete embedding implementation isolated from
    the application layer.
    """

    def __init__(
        self,
        embedding_model: Any,
    ) -> None:
        self.embedding_model = embedding_model

    def embed_documents(
        self,
        documents: list[str],
    ) -> list[list[float]]:
        if not documents:
            return []

        return self.embedding_model.embed_documents(
            documents
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        if not query or not query.strip():
            return []

        return self.embedding_model.embed_query(
            query
        )

