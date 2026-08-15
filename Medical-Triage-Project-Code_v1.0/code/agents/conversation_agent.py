from extractors.age_extractor import extract_age
from extractors.symptom_extractor import extract_symptoms
from extractors.duration_extractor import extract_duration
from extractors.severity_extractor import extract_severity

from utils.text_normalizer import normalize_text


# =============================================================
# Active Triage Detection
# =============================================================

def _is_active_triage(state):
    """
    Determine whether the conversation is already inside
    an active medical triage flow.

    Important:
    A single extracted field such as severity must NOT
    automatically start a triage flow.

    Active triage requires stronger evidence:
    - explicit TRIAGE intent
    - existing symptoms
    - missing triage information
    - an active next question
    """

    # ---------------------------------------------------------
    # Explicit intent
    # ---------------------------------------------------------

    if state.get("intent") == "TRIAGE":
        return True

    # ---------------------------------------------------------
    # Existing symptoms
    # ---------------------------------------------------------

    if state.get("symptoms"):
        return True

    # ---------------------------------------------------------
    # Planner is waiting for required information
    # ---------------------------------------------------------

    if state.get("missing_information"):
        return True

    # ---------------------------------------------------------
    # Agent has already asked a triage question
    # ---------------------------------------------------------

    if state.get("next_question") is not None:
        return True

    return False


# =============================================================
# Intent Detection
# =============================================================

def _detect_intent(state, message):
    """
    Detect the intent of the current user message.

    Priority:

    1. Existing active triage
    2. Explicit medical information in current message
    3. General conversation
    """

    # ---------------------------------------------------------
    # Existing triage has priority
    # ---------------------------------------------------------

    if _is_active_triage(state):
        return "TRIAGE", 1.0

    # ---------------------------------------------------------
    # Normalize message
    # ---------------------------------------------------------

    text = normalize_text(message)

    if not text:
        return "GENERAL", 1.0

    # ---------------------------------------------------------
    # Detect medical information
    # ---------------------------------------------------------

    symptoms = extract_symptoms(text)

    if symptoms:
        return "TRIAGE", 1.0

    age = extract_age(text)

    if age is not None:
        return "TRIAGE", 0.9

    duration = extract_duration(text)

    if duration is not None:
        return "TRIAGE", 0.9

    # ---------------------------------------------------------
    # IMPORTANT:
    # Severity alone should NOT start triage.
    #
    # Example:
    # "حالم خوبه"
    # "شدت صدا زیاده"
    #
    # A severity extractor may accidentally match
    # unrelated language.
    # ---------------------------------------------------------

    severity = extract_severity(text)

    if severity is not None and symptoms:
        return "TRIAGE", 0.9

    # ---------------------------------------------------------
    # Otherwise GENERAL
    # ---------------------------------------------------------

    return "GENERAL", 0.9


# =============================================================
# Conversation Agent
# =============================================================

def conversation_agent(
    state,
    llm_service=None,
    short_term_memory_service=None,
):
    """
    Process one conversation turn.

    Responsibilities:

    - preserve conversation history
    - store current patient message
    - detect intent
    - keep triage follow-up answers inside TRIAGE
    """

    message = state.get("user_message", "")

    if not isinstance(message, str):
        message = str(message)

    message = message.strip()

    # ---------------------------------------------------------
    # Conversation history
    # ---------------------------------------------------------

    history = list(
        state.get("conversation_history") or []
    )

    # ---------------------------------------------------------
    # Store current patient message
    # ---------------------------------------------------------

    if message:
        history.append(
            {
                "sender_type": "Patient",
                "content": message,
            }
        )

    # ---------------------------------------------------------
    # Detect intent
    # ---------------------------------------------------------

    intent, confidence = _detect_intent(
        state,
        message,
    )

    # ---------------------------------------------------------
    # Return updated state
    # ---------------------------------------------------------

    return {
        **state,
        "conversation_history": history,
        "intent": intent,
        "intent_confidence": confidence,
        "assistant_response": None,
    }