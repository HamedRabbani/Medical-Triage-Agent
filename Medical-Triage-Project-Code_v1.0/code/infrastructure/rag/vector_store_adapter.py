
from abc import ABC, abstractmethod
from typing import Any


class VectorStoreAdapter(ABC):
    """
    Application-independent abstraction for vector storage.
    """

    @abstractmethod
    def add_documents(
        self,
        documents: list[dict],
        embeddings: list[list[float]],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        raise NotImplementedError

