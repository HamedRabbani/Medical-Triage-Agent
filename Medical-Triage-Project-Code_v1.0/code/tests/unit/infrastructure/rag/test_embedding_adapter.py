from infrastructure.rag.embedding_adapter import (
    EmbeddingAdapter,
)


class FakeEmbeddingModel:

    def embed_documents(
        self,
        texts,
    ):
        return [
            [1.0, 2.0],
            [3.0, 4.0],
        ]

    def embed_query(
        self,
        text,
    ):
        return [5.0, 6.0]


def test_embedding_adapter_embeds_documents():

    adapter = EmbeddingAdapter(
        embedding_model=FakeEmbeddingModel()
    )

    result = adapter.embed_documents(
        [
            "headache",
            "fever",
        ]
    )

    assert result == [
        [1.0, 2.0],
        [3.0, 4.0],
    ]


def test_embedding_adapter_embeds_query():

    adapter = EmbeddingAdapter(
        embedding_model=FakeEmbeddingModel()
    )

    result = adapter.embed_query(
        "headache"
    )

    assert result == [
        5.0,
        6.0,
    ]