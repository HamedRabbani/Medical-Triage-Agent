from enum import Enum


class ConversationIntent(str, Enum):
    GENERAL = "GENERAL"
    TRIAGE = "TRIAGE"


def intent_router(state):
    """
    Route user input between general conversation and medical triage.

    This is intentionally rule-based for now.
    """

    message = state.get("user_message", "").lower().strip()

    if not message:
        return {
            **state,
            "intent": ConversationIntent.GENERAL.value,
        }

    medical_keywords = [
        "pain",
        "chest",
        "fever",
        "cough",
        "headache",
        "bleeding",
        "vomiting",
        "dizzy",
        "breathing",
        "shortness of breath",
        "درد",
        "تب",
        "سرفه",
        "سردرد",
        "خونریزی",
        "استفراغ",
        "سرگیجه",
        "نفس",
        "تنگی نفس",
        "قفسه سینه",
    ]

    if any(keyword in message for keyword in medical_keywords):
        return {
            **state,
            "intent": ConversationIntent.TRIAGE.value,
        }

    return {
        **state,
        "intent": ConversationIntent.GENERAL.value,
    }