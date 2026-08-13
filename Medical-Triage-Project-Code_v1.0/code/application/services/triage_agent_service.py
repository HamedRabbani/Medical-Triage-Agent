from application.services.triage_service import TriageService


class TriageAgentService:
    """Bridge between LangGraph and the application layer."""

    def __init__(self, triage_service: TriageService):
        self.triage_service = triage_service

    def save_triage_result(
        self,
        patient_id: int,
        content: str,
        risk_level: str,
        confidence_score: float,
        recommendation: str,
    ):
        """Persist Agent triage output."""

        return self.triage_service.process_triage(
            patient_id=patient_id,
            content=content,
            risk_level=risk_level,
            confidence_score=confidence_score,
            recommendation=recommendation,
        )