from datetime import UTC, datetime

from application.ports.triage_persistence_port import (
    TriagePersistencePort,
)

from infrastructure.database.models.conversation_msg import (
    ConversationMsg,
)
from infrastructure.database.models.triage_result import (
    TriageResult,
)
from infrastructure.database.models.triage_session import (
    TriageSession,
)
from infrastructure.database.unit_of_work import UnitOfWork


class SQLTriagePersistenceRepository(
    TriagePersistencePort
):
    """SQL Server implementation of triage persistence."""

    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow

    # =========================================================
    # Patient
    # =========================================================

    def patient_exists(
        self,
        patient_id: int,
    ) -> bool:
        return (
            self.uow.patients.get_by_id(patient_id)
            is not None
        )

    # =========================================================
    # Session
    # =========================================================

    def create_session(
        self,
        patient_id: int,
    ) -> TriageSession:

        triage_session = TriageSession(
            patient_id=patient_id,
            start_time=datetime.now(UTC),
            status="Active",
        )

        self.uow.triage.add(
            triage_session
        )

        return triage_session

    def get_session(
        self,
        session_id: int,
    ) -> TriageSession | None:

        return self.uow.triage.get_by_id(
            session_id
        )

    # =========================================================
    # Message
    # =========================================================

    def add_message(
        self,
        session_id: int,
        sender_type: str,
        content: str,
    ) -> ConversationMsg:

        message = ConversationMsg(
            session_id=session_id,
            sender_type=sender_type,
            content=content,
            timestamp=datetime.now(UTC),
        )

        self.uow.triage.add_message(
            message
        )

        return message

    # =========================================================
    # Result
    # =========================================================

    def add_result(
        self,
        session_id: int,
        risk_level: str,
        confidence_score: float,
        recommendation: str,
    ) -> TriageResult:

        result = TriageResult(
            session_id=session_id,
            risk_level=risk_level,
            confidence_score=confidence_score,
            recommendation=recommendation,
            created_at=datetime.now(UTC),
        )

        self.uow.triage.add_result(
            result
        )

        return result

    def get_results_by_patient_id(
        self,
        patient_id: int,
    ) -> list[TriageResult]:
        """Return previous triage results for a patient."""

        return self.uow.triage.get_results_by_patient_id(
            patient_id
        )

    # =========================================================
    # Transaction
    # =========================================================

    def commit(self) -> None:
        self.uow.commit()

    def rollback(self) -> None:
        self.uow.rollback()