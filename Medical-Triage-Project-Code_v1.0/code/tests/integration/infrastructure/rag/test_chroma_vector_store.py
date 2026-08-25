from infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)


def test_chroma_vector_store_add_and_search(
    tmp_path,
):

    store = ChromaVectorStore(
        collection_name="test_medical_knowledge",
        persist_directory=str(tmp_path),
    )

    documents = [
        {
            "chunk_id": "doc-1",
            "source": "medical.txt",
            "content": "Headache can have many causes.",
        },
        {
            "chunk_id": "doc-2",
            "source": "medical.txt",
            "content": "Fever is an elevated body temperature.",
        },
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]

    store.add(
        documents=documents,
        embeddings=embeddings,
    )

    results = store.search(
        embedding=[1.0, 0.0, 0.0],
        top_k=1,
    )

    assert len(results) == 1

    assert (
        results[0]["content"]
        == "Headache can have many causes."
    )

    assert (
        results[0]["source"]
        == "medical.txt"
    )