from typing import Protocol


class ConversationPersistencePort(Protocol):
    """Application contract for conversation persistence."""

    def create_session(
        self,
        patient_id: int,
    ) -> int:
        ...

    def add_message(
        self,
        session_id: int,
        content: str,
        sender_type: str = "Patient",
    ) -> dict:
        ...

    def get_history(
        self,
        session_id: int,
    ) -> list[dict]:
        ...