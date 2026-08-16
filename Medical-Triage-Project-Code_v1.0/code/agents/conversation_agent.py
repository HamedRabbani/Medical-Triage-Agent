from application.contracts.conversation_extraction import (
    ConversationExtraction,
)

from application.contracts.conversation_intent import (
    ConversationIntent,
)

from extractors.age_extractor import extract_age
from extractors.symptom_extractor import extract_symptoms
from extractors.duration_extractor import extract_duration
from extractors.severity_extractor import extract_severity

from utils.text_normalizer import normalize_text


INTENT_SYSTEM_PROMPT = """
You are the intent classifier of a medical triage system.

Classify the user's message into exactly one intent:

TRIAGE
GENERAL

TRIAGE:
- The user reports symptoms.
- The user provides medical information.
- The user answers a medical triage question.
- The user explicitly asks for medical assessment.

GENERAL:
- Greetings.
- Casual conversation.
- Non-medical questions.
- Normal conversation.

Return structured output only.
"""


EXTRACTION_SYSTEM_PROMPT = """
You are the medical information extraction component
of a medical triage system.

Extract ONLY information explicitly provided by the user.

Do not invent information.

Return structured output only.
"""


# =============================================================
# Active Triage Detection
# =============================================================

def _is_active_triage(state):

    if state.get("intent") == "TRIAGE":
        return True

    if state.get("symptoms"):
        return True

    if state.get("missing_information"):
        return True

    if state.get("next_question") is not None:
        return True

    return False


# =============================================================
# Deterministic Intent Detection
# =============================================================

def _detect_intent_from_message(
    state,
    message,
):
    """
    Deterministic baseline.

    Existing triage context always wins.

    Medical information explicitly present in the
    current message indicates TRIAGE.
    """

    if _is_active_triage(state):
        return "TRIAGE", 1.0

    text = normalize_text(
        message
    )

    if not text:
        return "GENERAL", 0.9

    symptoms = extract_symptoms(
        text
    )

    if symptoms:
        return "TRIAGE", 1.0

    age = extract_age(
        text
    )

    if age is not None:
        return "TRIAGE", 0.9

    duration = extract_duration(
        text
    )

    if duration is not None:
        return "TRIAGE", 0.9

    return "GENERAL", 0.9


# =============================================================
# Conversation Agent
# =============================================================

def conversation_agent(
    state,
    llm_service=None,
    short_term_memory_service=None,
):

    message = state.get(
        "user_message",
        "",
    )

    if not isinstance(
        message,
        str,
    ):
        message = str(message)

    message = message.strip()

    # =========================================================
    # Conversation History
    # =========================================================

    history = list(
        state.get(
            "conversation_history"
        )
        or []
    )

    if message:

        history.append(
            {
                "sender_type": "Patient",
                "content": message,
            }
        )

    # =========================================================
    # Deterministic Baseline
    # =========================================================

    detected_intent, detected_confidence = (
        _detect_intent_from_message(
            state,
            message,
        )
    )

    # =========================================================
    # No LLM
    # =========================================================

    if llm_service is None:

        return {
            **state,
            "conversation_history": history,
            "intent": detected_intent,
            "intent_confidence": detected_confidence,
            "assistant_response": None,
        }

    # =========================================================
    # Existing Active Triage
    # =========================================================

    if _is_active_triage(state):

        return {
            **state,
            "conversation_history": history,
            "intent": "TRIAGE",
            "intent_confidence": 1.0,
            "assistant_response": None,
        }

    # =========================================================
    # Intent Classification
    # =========================================================

    intent_result = llm_service.generate_structured(
        prompt=f"""
Classify this user message:

{message}
""",
        response_model=ConversationIntent,
        system_prompt=INTENT_SYSTEM_PROMPT,
    )

    if not isinstance(
        intent_result,
        ConversationIntent,
    ):
        raise TypeError(
            "Conversation intent must return "
            "ConversationIntent."
        )

    llm_intent = str(
        intent_result.intent
    ).upper()

    llm_confidence = (
        intent_result.confidence
    )

    # =========================================================
    # Deterministic Medical Override
    #
    # Safety baseline wins over LLM GENERAL classification.
    # =========================================================

    if detected_intent == "TRIAGE":

        intent = "TRIAGE"

        confidence = max(
            detected_confidence,
            llm_confidence or 0.0,
        )

    else:

        intent = llm_intent

        confidence = (
            llm_confidence
            if llm_confidence is not None
            else detected_confidence
        )

    # =========================================================
    # GENERAL
    # =========================================================

    if intent == "GENERAL":

        return {
            **state,
            "conversation_history": history,
            "intent": "GENERAL",
            "intent_confidence": confidence,
            "assistant_response": None,
        }

    # =========================================================
    # TRIAGE Extraction
    # =========================================================

    extraction_result = llm_service.generate_structured(
        prompt=f"""
Extract medical information from:

{message}
""",
        response_model=ConversationExtraction,
        system_prompt=EXTRACTION_SYSTEM_PROMPT,
    )

    if not isinstance(
        extraction_result,
        ConversationExtraction,
    ):
        raise TypeError(
            "Conversation extraction must return "
            "ConversationExtraction."
        )

    # =========================================================
    # Symptoms
    # =========================================================

    existing_symptoms = list(
        state.get("symptoms")
        or []
    )

    extracted_symptoms = list(
        extraction_result.symptoms
        or []
    )

    symptoms = list(
        dict.fromkeys(
            existing_symptoms
            + extracted_symptoms
        )
    )

    # =========================================================
    # Age
    # =========================================================

    age = extraction_result.age

    if age is None:

        age = extract_age(
            normalize_text(message)
        )

    if age is None:
        age = state.get("age")

    # =========================================================
    # Severity
    # =========================================================

    severity = extraction_result.severity

    if severity is None:

        severity = extract_severity(
            normalize_text(message)
        )

    if severity is None:
        severity = state.get(
            "severity"
        )

    # =========================================================
    # Duration
    # =========================================================

    duration = extraction_result.duration

    if duration is None:

        duration = extract_duration(
            normalize_text(message)
        )

    if duration is None:
        duration = state.get(
            "duration"
        )

    # =========================================================
    # Red Flags
    # =========================================================

    red_flags = list(
        dict.fromkeys(
            list(
                state.get("red_flags")
                or []
            )
            + list(
                extraction_result.red_flags
                or []
            )
        )
    )

    # =========================================================
    # Return
    # =========================================================

    return {
        **state,
        "conversation_history": history,
        "intent": "TRIAGE",
        "intent_confidence": confidence,
        "symptoms": symptoms,
        "age": age,
        "severity": severity,
        "duration": duration,
        "red_flags": red_flags,
        "assistant_response": None,
    }