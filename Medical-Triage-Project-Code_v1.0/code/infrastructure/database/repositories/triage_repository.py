from infrastructure.database.models.conversation_msg import (
    ConversationMsg,
)
from infrastructure.database.models.triage_result import (
    TriageResult,
)
from infrastructure.database.models.triage_session import (
    TriageSession,
)


class TriageRepository:
    """Repository for triage-related data."""

    def __init__(self, session):
        self.session = session

    # -------------------------
    # Triage Session
    # -------------------------

    def get_all(self) -> list[TriageSession]:
        """Get all triage sessions."""

        return (
            self.session
            .query(TriageSession)
            .all()
        )

    def get_by_id(
        self,
        session_id: int,
    ) -> TriageSession | None:
        """Get triage session by ID."""

        return (
            self.session
            .query(TriageSession)
            .filter(
                TriageSession.session_id == session_id
            )
            .first()
        )

    def get_by_patient_id(
        self,
        patient_id: int,
    ) -> list[TriageSession]:
        """Get all triage sessions for a patient."""

        return (
            self.session
            .query(TriageSession)
            .filter(
                TriageSession.patient_id == patient_id
            )
            .all()
        )

    def add(
        self,
        entity: TriageSession,
    ) -> TriageSession:
        """Add a triage session."""

        self.session.add(entity)
        self.session.flush()

        return entity

    # -------------------------
    # Conversation Message
    # -------------------------

    def add_message(
        self,
        message: ConversationMsg,
    ) -> ConversationMsg:
        """Add a conversation message."""

        self.session.add(message)
        self.session.flush()

        return message

    def get_messages(
        self,
        session_id: int,
    ) -> list[ConversationMsg]:
        """Get messages for a triage session."""

        return (
            self.session
            .query(ConversationMsg)
            .filter(
                ConversationMsg.session_id == session_id
            )
            .all()
        )

    # -------------------------
    # Triage Result
    # -------------------------

    def add_result(
        self,
        result: TriageResult,
    ) -> TriageResult:
        """Add a triage result."""

        self.session.add(result)
        self.session.flush()

        return result

    def get_result(
        self,
        session_id: int,
    ) -> TriageResult | None:
        """Get the first triage result for a session."""

        return (
            self.session
            .query(TriageResult)
            .filter(
                TriageResult.session_id == session_id
            )
            .first()
        )

    def get_results(
        self,
        session_id: int,
    ) -> list[TriageResult]:
        """Get all triage results for a session."""

        return (
            self.session
            .query(TriageResult)
            .filter(
                TriageResult.session_id == session_id
            )
            .all()
        )

    def get_results_by_patient_id(
        self,
        patient_id: int,
    ) -> list[TriageResult]:
        """Get all triage results for a patient."""

        return (
            self.session
            .query(TriageResult)
            .join(TriageSession)
            .filter(
                TriageSession.patient_id == patient_id
            )
            .order_by(
                TriageResult.created_at.desc()
            )
            .all()
        )