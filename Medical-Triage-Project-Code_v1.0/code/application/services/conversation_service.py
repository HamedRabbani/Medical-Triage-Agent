from application.ports.conversation_history_port import (
    ConversationHistoryPort,
)


class ConversationService:
    """Application service for conversation history."""

    def __init__(
        self,
        history_repository: ConversationHistoryPort,
    ):
        self.history_repository = history_repository

    def get_history(
        self,
        session_id: int,
    ) -> list[dict]:
        """Return conversation history for a session."""

        return self.history_repository.get_history(
            session_id
        )