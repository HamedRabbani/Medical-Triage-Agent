from application.services.triage_service import TriageService


class TriageAgentService:
    """Bridge between LangGraph and application services."""

    def __init__(self, triage_service: TriageService):
        self.triage_service = triage_service

    def create_session(
        self,
        patient_id: int,
    ):
        """Create a new triage session."""

        session = self.triage_service.start_session(
            patient_id
        )

        self.triage_service.uow.commit()

        return session

    def add_message(
        self,
        session_id: int,
        content: str,
        sender_type: str = "Patient",
    ):
        """Persist a conversation message."""

        message = self.triage_service.add_message(
            session_id=session_id,
            sender_type=sender_type,
            content=content,
        )

        self.triage_service.uow.commit()

        return message

    def save_triage_result(
        self,
        patient_id: int,
        content: str,
        risk_level: str,
        confidence_score: float,
        recommendation: str,
        session_id: int | None = None,
    ):
        """Persist final triage result."""

        return self.triage_service.process_triage(
            patient_id=patient_id,
            content=content,
            risk_level=risk_level,
            confidence_score=confidence_score,
            recommendation=recommendation,
            session_id=session_id,
        )