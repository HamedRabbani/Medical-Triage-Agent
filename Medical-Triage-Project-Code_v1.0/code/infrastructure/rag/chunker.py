class TextChunker:
    """
    Split medical documents into overlapping text chunks.

    Public API:
        chunk(documents)
        split(documents)  # backward-compatible alias
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 120,
    ) -> None:

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than zero."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller "
                "than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(
        self,
        documents: list[dict],
    ) -> list[dict]:

        chunks: list[dict] = []

        for document in documents:

            content = str(
                document.get(
                    "content",
                    "",
                )
            )

            if not content.strip():
                continue

            source = document.get("source")

            base_id = str(
                document.get(
                    "id",
                    document.get(
                        "chunk_id",
                        source or "document",
                    ),
                )
            )

            metadata = dict(
                document.get(
                    "metadata",
                    {},
                )
            )

            start = 0
            chunk_index = 0

            while start < len(content):

                end = min(
                    start + self.chunk_size,
                    len(content),
                )

                chunk_content = (
                    content[start:end].strip()
                )

                if chunk_content:

                    chunks.append(
                        {
                            "id": (
                                f"{base_id}"
                                f"::chunk-{chunk_index}"
                            ),
                            "content": chunk_content,
                            "source": source,
                            "metadata": {
                                **metadata,
                                "chunk_index": chunk_index,
                            },
                        }
                    )

                if end >= len(content):
                    break

                start = (
                    end
                    - self.chunk_overlap
                )

                chunk_index += 1

        return chunks

    def split(
        self,
        documents: list[dict],
    ) -> list[dict]:
        """
        Backward-compatible alias for chunk().
        """
        return self.chunk(documents)


class DocumentChunker(TextChunker):
    """
    Backward-compatible public name.

    Keeps existing tests and callers working while
    TextChunker remains the canonical implementation.
    """

    pass