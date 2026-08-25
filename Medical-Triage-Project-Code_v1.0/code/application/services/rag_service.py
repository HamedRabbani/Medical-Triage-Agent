from application.ports.rag_port import RAGPort


class RAGService:
    """
    Application service for Retrieval-Augmented Generation.

    Depends only on RAGPort.
    """

    def __init__(
        self,
        rag_repository: RAGPort,
    ):
        self.rag_repository = rag_repository

    def add_documents(
        self,
        documents: list[dict],
    ) -> None:

        self.rag_repository.add_documents(
            documents
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        distance_threshold: float | None = None,
    ) -> list[dict]:

        if not query or not query.strip():
            return []

        return self.rag_repository.retrieve(
            query=query,
            top_k=top_k,
            distance_threshold=distance_threshold,
        )