from typing import Literal


ConversationIntent = Literal[
    "TRIAGE",
    "GENERAL",
]


TRIAGE_KEYWORDS = {
    "pain",
    "ache",
    "fever",
    "cough",
    "headache",
    "nausea",
    "vomiting",
    "dizziness",
    "shortness of breath",
    "chest pain",
    "bleeding",
    "fainting",
    "loss of consciousness",
    "تب",
    "سرفه",
    "سردرد",
    "تهوع",
    "استفراغ",
    "سرگیجه",
    "درد",
    "درد قفسه سینه",
    "تنگی نفس",
    "خونریزی",
    "بیهوشی",
}


def conversation_intent(state) -> dict:
    """
    Classify the current user message as TRIAGE or GENERAL.
    """

    text = state.get("user_message", "")

    if not isinstance(text, str):
        return {
            **state,
            "intent": "GENERAL",
        }

    normalized_text = text.strip().lower()

    if not normalized_text:
        return {
            **state,
            "intent": "GENERAL",
        }

    for keyword in TRIAGE_KEYWORDS:
        if keyword in normalized_text:
            return {
                **state,
                "intent": "TRIAGE",
            }

    return {
        **state,
        "intent": "GENERAL",
    }