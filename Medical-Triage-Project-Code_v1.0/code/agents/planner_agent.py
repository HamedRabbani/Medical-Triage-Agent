def planner_agent(state):
    """
    Determine which patient information is missing.

    The planner reports missing information.

    It does NOT decide whether risk assessment should stop.

    Pain location is required when the user reports
    generic pain without specifying where the pain is.
    """

    missing = []

    symptoms = list(
        state.get("symptoms")
        or []
    )

    pain_location = state.get(
        "pain_location"
    )

    # =========================================================
    # Pain Location
    # =========================================================
    #
    # If the user says something like:
    #
    #     "درد دارم"
    #
    # the symptom extractor may produce:
    #
    #     ["general pain"]
    #
    # Therefore we must ask where the pain is.
    #
    # If the user already said:
    #
    #     "درد شکم دارم"
    #
    # pain_location should already be populated and
    # this question will be skipped.
    # =========================================================

    if (
        "general pain" in symptoms
        and not pain_location
    ):
        missing.append(
            "pain_location"
        )

    # =========================================================
    # Age
    # =========================================================

    if state.get("age") is None:

        missing.append(
            "age"
        )

    # =========================================================
    # Symptoms
    # =========================================================

    if not symptoms:

        missing.append(
            "symptoms"
        )

    # =========================================================
    # Duration
    # =========================================================

    if state.get("duration") is None:

        missing.append(
            "duration"
        )

    # =========================================================
    # Severity
    # =========================================================

    if state.get("severity") is None:

        missing.append(
            "severity"
        )

    # =========================================================
    # Questions
    # =========================================================

    questions = {

        "pain_location": (
            "Where exactly is the pain? / "
            "دردتان دقیقاً کجاست؟"
        ),

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

    # =========================================================
    # Next Question
    # =========================================================

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

        "immediate_high_risk": (
            immediate_high_risk
        ),
    }