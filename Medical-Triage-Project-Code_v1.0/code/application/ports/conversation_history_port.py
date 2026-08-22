from typing import Protocol


class ConversationHistoryPort(Protocol):
    """Application contract for conversation history persistence."""

    def get_history(
        self,
        session_id: int,
    ) -> list[dict]:
        ...