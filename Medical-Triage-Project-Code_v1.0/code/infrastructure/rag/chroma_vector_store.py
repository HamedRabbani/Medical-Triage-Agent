from pathlib import Path
from typing import Any

import chromadb

from infrastructure.rag.vector_store_adapter import (
    VectorStoreAdapter,
)


class ChromaVectorStore(VectorStoreAdapter):
    """
    ChromaDB-backed vector store.

    Responsibilities:
    - Persist vectors locally.
    - Store document content and metadata.
    - Execute similarity search.

    Canonical API:
        add_documents()
        similarity_search()

    Backward-compatible API:
        add()
        search()
    """

    def __init__(
        self,
        collection_name: str,
        persist_directory: str,
    ) -> None:

        self.persist_directory = Path(
            persist_directory
        )

        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name,
                metadata={
                    "hnsw:space": "cosine",
                },
            )
        )

    def add_documents(
        self,
        documents: list[dict],
        embeddings: list[list[float]],
    ) -> None:

        if not documents:
            return

        if len(documents) != len(embeddings):
            raise ValueError(
                "documents and embeddings must have "
                "the same length."
            )

        ids: list[str] = []
        texts: list[str] = []
        metadatas: list[dict[str, Any]] = []
        vectors: list[list[float]] = []

        for index, document in enumerate(
            documents
        ):

            document_id = str(
                document.get(
                    "id",
                    document.get(
                        "chunk_id",
                        f"document-{index}",
                    ),
                )
            )

            content = str(
                document.get(
                    "content",
                    "",
                )
            )

            if not content.strip():
                continue

            metadata = dict(
                document.get(
                    "metadata",
                    {},
                )
            )

            if "source" in document:
                metadata.setdefault(
                    "source",
                    document["source"],
                )

            ids.append(document_id)
            texts.append(content)
            metadatas.append(metadata)
            vectors.append(
                embeddings[index]
            )

        if not ids:
            return

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=vectors,
        )

    def add(
        self,
        documents: list[dict],
        embeddings: list[list[float]],
    ) -> None:
        """
        Backward-compatible alias for add_documents().
        """
        self.add_documents(
            documents=documents,
            embeddings=embeddings,
        )

    def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:

        if not query_embedding:
            return []

        if top_k <= 0:
            return []

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        documents = (
            result.get("documents", [[]])[0]
        )

        metadatas = (
            result.get("metadatas", [[]])[0]
        )

        distances = (
            result.get("distances", [[]])[0]
        )

        ids = (
            result.get("ids", [[]])[0]
        )

        output: list[dict] = []

        for index, content in enumerate(
            documents
        ):

            metadata = (
                metadatas[index]
                if index < len(metadatas)
                else {}
            )

            distance = (
                distances[index]
                if index < len(distances)
                else None
            )

            document_id = (
                ids[index]
                if index < len(ids)
                else None
            )

            output.append(
                {
                    "id": document_id,
                    "content": content,
                    "metadata": metadata or {},
                    "source": (
                        (metadata or {}).get(
                            "source"
                        )
                    ),
                    "distance": distance,
                }
            )

        return output

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        """
        Backward-compatible alias for
        similarity_search().
        """
        return self.similarity_search(
            query_embedding=embedding,
            top_k=top_k,
        )