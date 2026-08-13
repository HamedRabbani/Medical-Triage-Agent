from typing import TypedDict


class TriageState(TypedDict, total=False):
    # Session identity
    patient_id: int | None
    session_id: int | None

    # User input
    user_message: str

    # Extracted information
    age: int | None
    symptoms: list[str]
    severity: str | None
    duration: str | None

    # Risk assessment
    red_flags: list[str]
    missing_information: list[str]
    next_question: str | None

    risk_level: str | None
    confidence: float | None

    # Final decision
    supervisor_status: str | None
    recommendation: str | None

    conversation_history: list[dict]
    result_id: int | None