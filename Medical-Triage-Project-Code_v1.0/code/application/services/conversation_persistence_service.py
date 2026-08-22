from application.ports.conversation_persistence_port import (
    ConversationPersistencePort,
)


class ConversationPersistenceService:
    """Application service for conversation persistence."""

    def __init__(
        self,
        repository: ConversationPersistencePort,
    ):
        self.repository = repository

    def create_session(
        self,
        patient_id: int,
    ) -> int:
        return self.repository.create_session(
            patient_id
        )

    def add_message(
        self,
        session_id: int,
        content: str,
        sender_type: str = "Patient",
    ) -> dict:
        return self.repository.add_message(
            session_id=session_id,
            content=content,
            sender_type=sender_type,
        )

    def get_history(
        self,
        session_id: int,
    ) -> list[dict]:
        return self.repository.get_history(
            session_id
        )