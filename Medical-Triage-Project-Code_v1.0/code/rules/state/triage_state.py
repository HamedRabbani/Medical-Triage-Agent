from typing import TypedDict


class TriageState(TypedDict, total=False):
    user_message: str

    age: int | None
    symptoms: list[str]
    severity: str | None
    duration: str | None

    red_flags: list[str]

    missing_information: list[str]
    next_question: str | None

    risk_level: str | None
    confidence: float | None

    llm_risk_level: str | None
    llm_confidence: float | None
    llm_red_flags: list[str]
    llm_recommendation: str | None

    supervisor_status: str | None
    recommendation: str | None
    