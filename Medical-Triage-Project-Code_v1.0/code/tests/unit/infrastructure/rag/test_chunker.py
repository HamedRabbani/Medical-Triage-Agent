from infrastructure.rag.chunker import TextChunker


def test_chunker_splits_document():

    documents = [
        {
            "source": "medical.txt",
            "content": "abcdefghij",
        }
    ]

    chunker = TextChunker(
        chunk_size=5,
        chunk_overlap=2,
    )

    chunks = chunker.chunk(documents)

    assert len(chunks) == 3

    assert chunks[0]["content"] == "abcde"
    assert chunks[1]["content"] == "defgh"
    assert chunks[2]["content"] == "ghij"


def test_chunker_rejects_invalid_configuration():

    try:
        TextChunker(
            chunk_size=10,
            chunk_overlap=10,
        )
        assert False
    except ValueError:
        assert True