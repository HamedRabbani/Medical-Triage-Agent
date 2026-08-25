
from langchain_huggingface import (
    HuggingFaceEmbeddings,
)

from application.services.rag_service import (
    RAGService,
)

from infrastructure.rag.embedding_adapter import (
    EmbeddingAdapter,
)

from infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)

from infrastructure.rag.rag_repository_adapter import (
    RAGRepositoryAdapter,
)


EMBEDDING_MODEL = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

CHROMA_COLLECTION = "medical_knowledge"
CHROMA_DIRECTORY = "data/chroma"


def create_rag_service() -> RAGService:

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    embedding_adapter = EmbeddingAdapter(
        embedding_model=embedding_model
    )

    vector_store = ChromaVectorStore(
        collection_name=CHROMA_COLLECTION,
        persist_directory=CHROMA_DIRECTORY,
    )

    rag_repository = RAGRepositoryAdapter(
        embedding_service=embedding_adapter,
        vector_store=vector_store,
    )

    return RAGService(
        rag_repository=rag_repository,
    )

