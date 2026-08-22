from typing import Protocol


class TriagePersistencePort(Protocol):
    """Application contract for triage persistence."""

    def patient_exists(
        self,
        patient_id: int,
    ) -> bool:
        ...

    def create_session(
        self,
        patient_id: int,
    ):
        ...

    def get_session(
        self,
        session_id: int,
    ):
        ...

    def add_message(
        self,
        session_id: int,
        sender_type: str,
        content: str,
    ):
        ...

    def add_result(
        self,
        session_id: int,
        risk_level: str,
        confidence_score: float,
        recommendation: str,
    ):
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...