from typing import TypedDict

from application.contracts.short_term_memory import (
    ShortTermMemory,
)


class TriageState(TypedDict, total=False):

    # =====================================================
    # Patient / Session
    # =====================================================

    patient_id: int | None
    session_id: int | None

    # =====================================================
    # Input
    # =====================================================

    user_message: str

    # =====================================================
    # Extracted Patient Information
    # =====================================================

    age: int | None
    symptoms: list[str]
    severity: str | None
    duration: str | None

    # =====================================================
    # Rule-Based Risk Assessment
    # =====================================================

    red_flags: list[str]

    risk_level: str | None
    confidence: float | None
    recommendation: str | None

    # =====================================================
    # Planner
    # =====================================================

    missing_information: list[str]
    next_question: str | None

    # =====================================================
    # LLM Risk Assessment
    # =====================================================

    llm_risk_level: str | None
    llm_confidence: float | None
    llm_red_flags: list[str] | None
    llm_recommendation: str | None

    # =====================================================
    # Supervisor
    # =====================================================

    supervisor_status: str | None

    # =====================================================
    # Conversation
    # =====================================================

    conversation_history: list[dict]

    intent: str | None
    intent_confidence: float | None

    triage_active: bool
    
    assistant_response: str | None
    response: str | None

    # =====================================================
    # Persistence
    # =====================================================

    result_id: int | None

    # =====================================================
    # Memory
    # =====================================================

    short_term_memory: ShortTermMemory | None