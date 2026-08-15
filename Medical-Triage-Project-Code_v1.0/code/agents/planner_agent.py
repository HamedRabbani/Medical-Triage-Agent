def planner_agent(state):
    """
    Determine which patient information is missing.

    The planner reports missing information.
    It does NOT decide whether risk assessment must stop.
    """

    missing = []

    if state.get("age") is None:
        missing.append("age")

    if not state.get("symptoms"):
        missing.append("symptoms")

    if state.get("duration") is None:
        missing.append("duration")

    if state.get("severity") is None:
        missing.append("severity")

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
        next_question = questions[missing[0]]

    return {
        **state,
        "missing_information": missing,
        "next_question": next_question,
    }