from langgraph.graph import END


def route_conversation(state):
    """
    Route the conversation based on the detected intent.
    """

    intent = state.get("intent")

    if intent == "TRIAGE":
        return "triage"

    if intent == "GENERAL":
        return "general"

    # Fail closed.
    # Unknown intent must never enter the medical pipeline.
    return "general"