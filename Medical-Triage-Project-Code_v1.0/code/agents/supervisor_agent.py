def supervisor_agent(state):

    risk = state.get("risk_level")
    confidence = state.get("confidence")

    if risk is None:
        return {
            **state,
            "supervisor_status": "REJECTED",
        }

    if confidence is None:
        return {
            **state,
            "supervisor_status": "REJECTED",
        }

    if risk == "HIGH" and not state.get("red_flags"):
        return {
            **state,
            "supervisor_status": "REVIEW_REQUIRED",
        }

    return {
        **state,
        "supervisor_status": "APPROVED",
    }