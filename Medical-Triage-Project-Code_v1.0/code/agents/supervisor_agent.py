def supervisor_agent(state):
    """
    Validate and compare rule-based and LLM-based triage assessments.

    Safety principle:
    - Rule-based assessment remains the safety baseline.
    - LLM assessment is a secondary evaluation layer.
    - Any disagreement requires human review.
    """

    # -------------------------
    # Rule-based assessment
    # -------------------------

    risk = state.get("risk_level")
    confidence = state.get("confidence")
    red_flags = state.get("red_flags") or []

    # -------------------------
    # LLM assessment
    # -------------------------

    llm_risk = state.get("llm_risk_level")
    llm_confidence = state.get("llm_confidence")
    llm_red_flags = state.get("llm_red_flags") or []

    # -------------------------
    # Basic validation
    # -------------------------

    if risk is None or confidence is None:
        return {
            **state,
            "supervisor_status": "REJECTED",
        }

    # -------------------------
    # LLM assessment missing
    # -------------------------

    if llm_risk is None or llm_confidence is None:
        return {
            **state,
            "supervisor_status": "REVIEW_REQUIRED",
        }

    # -------------------------
    # Rule vs LLM risk disagreement
    # -------------------------

    if risk != llm_risk:
        return {
            **state,
            "supervisor_status": "REVIEW_REQUIRED",
        }

    # -------------------------
    # Rule vs LLM red flag disagreement
    # -------------------------

    if set(red_flags) != set(llm_red_flags):
        return {
            **state,
            "supervisor_status": "REVIEW_REQUIRED",
        }

    # -------------------------
    # High risk without rule red flags
    # -------------------------

    if risk == "HIGH" and not red_flags:
        return {
            **state,
            "supervisor_status": "REVIEW_REQUIRED",
        }

    # -------------------------
    # Approved
    # -------------------------

    return {
        **state,
        "supervisor_status": "APPROVED",
    }