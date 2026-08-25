
from pathlib import Path


class DocumentLoader:
    """
    Load medical knowledge documents from disk.
    """

    def __init__(
        self,
        knowledge_directory: str = (
            "knowledge/medical"
        ),
    ) -> None:
        self.knowledge_directory = Path(
            knowledge_directory
        )

    def load(
        self,
    ) -> list[dict]:

        if not self.knowledge_directory.exists():
            return []

        documents: list[dict] = []

        for path in sorted(
            self.knowledge_directory.rglob("*.txt")
        ):
            content = path.read_text(
                encoding="utf-8"
            )

            if not content.strip():
                continue

            documents.append(
                {
                    "id": str(
                        path.relative_to(
                            self.knowledge_directory
                        )
                    ),
                    "content": content,
                    "source": str(path),
                    "metadata": {
                        "source": str(path),
                        "file_name": path.name,
                    },
                }
            )

        return documents

