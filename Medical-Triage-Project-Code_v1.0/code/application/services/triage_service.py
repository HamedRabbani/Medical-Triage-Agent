from datetime import datetime

from infrastructure.database.models.conversation_msg import ConversationMsg
from infrastructure.database.models.triage_result import TriageResult
from infrastructure.database.models.triage_session import TriageSession
from infrastructure.database.unit_of_work import UnitOfWork


class TriageService:
    """Application service for triage use cases."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def start_session(
        self,
        patient_id: int,
    ) -> TriageSession:
        """Create a new triage session."""

        patient = self.uow.patients.get_by_id(patient_id)

        if patient is None:
            raise ValueError(
                f"Patient {patient_id} does not exist."
            )

        triage_session = TriageSession(
            patient_id=patient_id,
            start_time=datetime.utcnow(),
            status="Active",
        )

        self.uow.triage.add(triage_session)

        return triage_session

    def add_message(
        self,
        session_id: int,
        sender_type: str,
        content: str,
    ) -> ConversationMsg:
        """Add a message to an existing triage session."""

        triage_session = self.uow.triage.get_by_id(
            session_id
        )

        if triage_session is None:
            raise ValueError(
                f"Triage session {session_id} does not exist."
            )

        message = ConversationMsg(
            session_id=session_id,
            sender_type=sender_type,
            content=content,
            timestamp=datetime.utcnow(),
        )

        self.uow.triage.add_message(message)

        return message

    def save_result(
        self,
        session_id: int,
        risk_level: str,
        confidence_score: float,
        recommendation: str,
    ) -> TriageResult:
        """Persist a triage result."""

        triage_session = self.uow.triage.get_by_id(
            session_id
        )

        if triage_session is None:
            raise ValueError(
                f"Triage session {session_id} does not exist."
            )

        result = TriageResult(
            session_id=session_id,
            risk_level=risk_level,
            confidence_score=confidence_score,
            recommendation=recommendation,
            created_at=datetime.utcnow(),
        )

        self.uow.triage.add_result(result)

        return result

    def process_triage(
        self,
        patient_id: int,
        content: str,
        risk_level: str,
        confidence_score: float,
        recommendation: str,
        session_id: int | None = None,
    ) -> dict:
        """Process triage using a new or existing session."""

        try:
            # ---------------------------------
            # Create a new session when needed
            # ---------------------------------
            if session_id is None:

                session = self.start_session(
                    patient_id
                )

                # Generate SessionId
                self.uow.session.flush()

                session_id = session.session_id

            # ---------------------------------
            # Verify existing session
            # ---------------------------------
            else:

                session = self.uow.triage.get_by_id(
                    session_id
                )

                if session is None:
                    raise ValueError(
                        f"Triage session "
                        f"{session_id} does not exist."
                    )

                if session.patient_id != patient_id:
                    raise ValueError(
                        "Session does not belong "
                        "to the specified patient."
                    )

            # ---------------------------------
            # Save final triage result
            # ---------------------------------
            result = self.save_result(
                session_id=session_id,
                risk_level=risk_level,
                confidence_score=confidence_score,
                recommendation=recommendation,
            )

            # ---------------------------------
            # Commit transaction
            # ---------------------------------
            self.uow.commit()

            return {
            "result_id": result.result_id,
            "session_id": result.session_id,
            "risk_level": result.risk_level,
            "confidence_score": result.confidence_score,
            "recommendation": result.recommendation,
        }

        except Exception:
            # ---------------------------------
            # Rollback transaction
            # ---------------------------------
            self.uow.rollback()
            raise