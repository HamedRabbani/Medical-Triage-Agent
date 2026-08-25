
from infrastructure.rag.rag_factory import (
    create_rag_service,
)

from infrastructure.rag.document_loader import (
    DocumentLoader,
)

from infrastructure.rag.chunker import (
    TextChunker,
)

from infrastructure.rag.rag_pipeline import (
    RAGPipeline,
)


def main() -> None:

    rag_service = create_rag_service()

    loader = DocumentLoader(
        knowledge_directory=(
            "knowledge/medical"
        )
    )

    chunker = TextChunker(
        chunk_size=800,
        chunk_overlap=120,
    )

    pipeline = RAGPipeline(
        rag_service=rag_service,
        document_loader=loader,
        chunker=chunker,
    )

    count = pipeline.ingest()

    print(
        f"Indexed {count} knowledge chunks."
    )


if __name__ == "__main__":
    main()

