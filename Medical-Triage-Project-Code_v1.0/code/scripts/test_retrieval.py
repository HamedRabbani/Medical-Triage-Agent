from infrastructure.rag.embedding_adapter import EmbeddingAdapter
from infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)
from infrastructure.rag.rag_repository_adapter import (
    RAGRepositoryAdapter,
)
from langchain_huggingface import HuggingFaceEmbeddings

def main():

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

    vector_store = ChromaVectorStore(
        collection_name="medical_knowledge",
        persist_directory="data/chroma",
    )

    rag_repository = RAGRepositoryAdapter(
        embedding_service=embedding_adapter,
        vector_store=vector_store,
    )

    queries = [
        "I have a severe headache",
        "من سردرد شدید دارم",
    ]

    for query in queries:

        print("\n" + "=" * 60)
        print(f"QUERY: {query}")
        print("=" * 60)

        results = rag_repository.retrieve(
            query=query,
            top_k=3,
        )

        for index, result in enumerate(
            results,
            start=1,
        ):

            print(f"\nResult {index}")
            print(f"Source: {result['source']}")
            print(
                f"Distance: {result['distance']}"
            )
            print(
                f"Content:\n{result['content']}"
            )


if __name__ == "__main__":
    main()