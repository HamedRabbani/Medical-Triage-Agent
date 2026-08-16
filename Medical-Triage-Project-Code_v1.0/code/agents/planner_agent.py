def planner_agent(state):
    """
    Determine which patient information is missing.

    The planner reports missing information.

    It does NOT decide whether risk assessment should stop.
    """

    missing = []

    # =========================================================
    # Required Information
    # =========================================================

    if state.get("age") is None:
        missing.append("age")

    if not state.get("symptoms"):
        missing.append("symptoms")

    if state.get("duration") is None:
        missing.append("duration")

    if state.get("severity") is None:
        missing.append("severity")

    # =========================================================
    # Questions
    # =========================================================

    questions = {
        "age": (
            "How old are you? / "
            "چند سال دارید؟"
        ),
        "symptoms": (
            "What symptoms are you experiencing? / "
            "چه علائمی دارید؟"
        ),
        "duration": (
            "How long have you had these symptoms? / "
            "چند وقت است این علائم را دارید؟"
        ),
        "severity": (
            "How severe are your symptoms? / "
            "شدت علائم چقدر است؟"
        ),
    }

    next_question = None

    if missing:

        next_question = questions[
            missing[0]
        ]

    # =========================================================
    # Immediate High-Risk Detection
    #
    # Do NOT remove next_question.
    # route_planner decides whether to skip it.
    # =========================================================

    symptoms = list(
        state.get("symptoms")
        or []
    )

    severity = state.get(
        "severity"
    )

    immediate_high_risk = False

    if (
        "chest pain" in symptoms
        and "shortness of breath" in symptoms
    ):
        immediate_high_risk = True

    if (
        "loss of consciousness"
        in symptoms
    ):
        immediate_high_risk = True

    if severity == "severe":
        immediate_high_risk = True

    # =========================================================
    # Return
    # =========================================================

    return {
        **state,
        "missing_information": missing,
        "next_question": next_question,
        "immediate_high_risk": immediate_high_risk,
    }