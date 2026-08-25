from typing import Protocol


class RAGPort(Protocol):
    """Port for Retrieval-Augmented Generation storage."""

    def add_documents(
        self,
        documents: list[dict],
    ) -> None:
        ...

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        distance_threshold: float | None = None,
    ) -> list[dict]:
        ...