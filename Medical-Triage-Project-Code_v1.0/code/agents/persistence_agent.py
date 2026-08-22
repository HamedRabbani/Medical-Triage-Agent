from application.services.triage_agent_service import (
    TriageAgentService,
)
from application.services.triage_service import (
    TriageService,
)


def persistence_agent(
    state,
    database_backend,
):
    """Persist final triage result."""

    patient_id = state.get("patient_id")
    session_id = state.get("session_id")

    risk_level = state.get("risk_level")
    confidence = state.get("confidence")
    recommendation = state.get("recommendation")

    if patient_id is None:
        return {
            **state,
            "supervisor_status": "REJECTED",
        }

    if session_id is None:
        return {
            **state,
            "supervisor_status": "REJECTED",
        }

    if risk_level is None or confidence is None:
        return {
            **state,
            "supervisor_status": "REJECTED",
        }

    if recommendation is None:
        recommendation = (
            "No recommendation available."
        )

    triage_service = TriageService(
        database_backend.triage
    )

    agent_service = TriageAgentService(
        triage_service
    )

    try:
        result = agent_service.save_triage_result(
            patient_id=patient_id,
            content=state.get(
                "user_message",
                "",
            ),
            risk_level=risk_level,
            confidence_score=confidence,
            recommendation=recommendation,
            session_id=session_id,
        )

        database_backend.triage.commit()

        return {
            **state,
            "session_id": result.session_id,
            "result_id": result.result_id,
        }

    except Exception:
        database_backend.triage.rollback()
        raise