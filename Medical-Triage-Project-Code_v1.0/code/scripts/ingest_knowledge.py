from infrastructure.rag.document_loader import DocumentLoader
from infrastructure.rag.chunker import DocumentChunker
from infrastructure.rag.embedding_adapter import EmbeddingAdapter
from infrastructure.rag.rag_repository_adapter import (
    RAGRepositoryAdapter,
)
from infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)
from infrastructure.rag.rag_pipeline import RAGPipeline


def main():

    # ---------------------------------------------------------
    # Load documents
    # ---------------------------------------------------------

    loader = DocumentLoader()

    documents = loader.load(
        "knowledge/medical"
    )

    if not documents:
        raise RuntimeError(
            "No knowledge documents found."
        )

    # ---------------------------------------------------------
    # Embedding provider
    # ---------------------------------------------------------

    from langchain_community.embeddings import (
        HuggingFaceEmbeddings,
    )

    embedding_model = HuggingFaceEmbeddings(
        model_name=(
            "sentence-transformers/"
            "paraphrase-multilingual-MiniLM-L12-v2"
        )
    )

    embedding_adapter = EmbeddingAdapter(
        embedding_model=embedding_model
    )

    # ---------------------------------------------------------
    # Vector store
    # ---------------------------------------------------------

    vector_store = ChromaVectorStore(
        collection_name="medical_knowledge",
        persist_directory="data/chroma",
    )

    # ---------------------------------------------------------
    # RAG repository
    # ---------------------------------------------------------

    rag_repository = RAGRepositoryAdapter(
        embedding_service=embedding_adapter,
        vector_store=vector_store,
    )

    # ---------------------------------------------------------
    # Pipeline
    # ---------------------------------------------------------

    pipeline = RAGPipeline(
        chunker=DocumentChunker(
            chunk_size=500,
            chunk_overlap=50,
        ),
        rag_repository=rag_repository,
    )

    # ---------------------------------------------------------
    # Ingest
    # ---------------------------------------------------------

    pipeline.ingest(documents)

    print(
        f"Ingested {len(documents)} document(s)."
    )


if __name__ == "__main__":
    main()