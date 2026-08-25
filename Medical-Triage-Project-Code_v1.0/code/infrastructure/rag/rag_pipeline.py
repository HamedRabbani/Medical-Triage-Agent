
from infrastructure.rag.document_loader import (
    DocumentLoader,
)

from infrastructure.rag.chunker import (
    TextChunker,
)

from application.services.rag_service import (
    RAGService,
)


class RAGPipeline:
    """
    Knowledge ingestion pipeline.

    Flow:

        Documents
            ↓
        Loader
            ↓
        Chunker
            ↓
        Embedding
            ↓
        VectorDB
    """

    def __init__(
        self,
        rag_service: RAGService,
        document_loader: DocumentLoader,
        chunker: TextChunker,
    ) -> None:

        self.rag_service = rag_service
        self.document_loader = document_loader
        self.chunker = chunker

    def ingest(self) -> int:

        documents = (
            self.document_loader.load()
        )

        if not documents:
            return 0

        chunks = self.chunker.chunk(
            documents
        )

        if not chunks:
            return 0

        self.rag_service.add_documents(
            chunks
        )

        return len(chunks)

