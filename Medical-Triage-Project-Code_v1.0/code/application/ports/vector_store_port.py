from typing import Protocol


class VectorStorePort(Protocol):

    def add(
        self,
        documents: list[dict],
        embeddings: list[list[float]],
    ) -> None:
        ...

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        ...