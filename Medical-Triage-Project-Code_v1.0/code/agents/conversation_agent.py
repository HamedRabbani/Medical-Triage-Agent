
import time

from application.contracts.conversation_extraction import (
    ConversationExtraction,
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
PROFILE

TRIAGE:
- The user reports symptoms.
- The user provides medical information.
- The user answers a medical triage question.
- The user explicitly asks for medical assessment.

PROFILE:
- The user asks about their own profile.
- The user asks what information the system knows about them.
- The user asks for their own age, role, account information,
  or personal information stored in their profile.
- The user asks to check or show their profile.

GENERAL:
- Greetings.
- Casual conversation.
- Non-medical questions.
- Normal conversation.

Important:
- PROFILE means the user's OWN profile.
- Do not infer another patient's information.
- Do not access or discuss another patient's information.

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
    """
    Determine whether the system is already inside
    an active medical triage flow.

    Active triage context has priority over the
    current message classification.
    """

    if state.get("missing_information"):
        return True

    if state.get("next_question") is not None:
        return True

    return False


# =============================================================
# Profile Intent Detection
# =============================================================

def _is_profile_request(text: str) -> bool:
    """
    Detect whether the user is asking about
    their own profile/account information.

    This is deterministic and does not require an LLM.
    """

    profile_keywords = [
        # Persian
        "پروفایل",
        "پروفایل من",
        "پروفایل منو",
        "پروفایل خودم",
        "اطلاعات من",
        "اطلاعات شخصی من",
        "اطلاعات حساب من",
        "اطلاعات کاربری من",
        "اطلاعاتی که از من داری",
        "چه اطلاعاتی از من داری",
        "مشخصات من",
        "سنم",
        "سن من",
        "نقشم",
        "نقش من",
        "حساب من",

        # English
        "my profile",
        "my account",
        "my information",
        "my personal information",
        "what do you know about me",
        "what information do you have about me",
        "check my profile",
        "show my profile",
        "my age",
        "my role",
    ]

    return any(
        keyword in text
        for keyword in profile_keywords
    )


# =============================================================
# Deterministic Intent Detection
# =============================================================

def _detect_intent_from_message(
    state,
    message,
):
    """
    Deterministic intent baseline.

    Priority:

    1. Active triage context
    2. Profile request
    3. Explicit medical information
    4. Otherwise GENERAL
    """

    # ---------------------------------------------------------
    # Existing active triage
    # ---------------------------------------------------------

    if _is_active_triage(state):
        return "TRIAGE", 1.0

    # ---------------------------------------------------------
    # Normalize message
    # ---------------------------------------------------------

    text = normalize_text(message)

    if not text:
        return "GENERAL", 0.9

    # ---------------------------------------------------------
    # Profile detection
    # ---------------------------------------------------------

    if _is_profile_request(text):
        return "PROFILE", 1.0

    # ---------------------------------------------------------
    # Symptom detection
    # ---------------------------------------------------------

    symptoms = extract_symptoms(text)

    if symptoms:
        return "TRIAGE", 1.0

    # ---------------------------------------------------------
    # Age detection
    # ---------------------------------------------------------

    age = extract_age(text)

    if age is not None:
        return "TRIAGE", 0.9

    # ---------------------------------------------------------
    # Duration detection
    # ---------------------------------------------------------

    duration = extract_duration(text)

    if duration is not None:
        return "TRIAGE", 0.9

    # ---------------------------------------------------------
    # Severity detection
    # ---------------------------------------------------------

    severity = extract_severity(text)

    if severity is not None:
        return "TRIAGE", 0.9

    # ---------------------------------------------------------
    # No explicit medical information
    # ---------------------------------------------------------

    return "GENERAL", 0.9


# =============================================================
# Conversation Agent
# =============================================================

def conversation_agent(
    state,
    llm_service=None,
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
    # Debug
    # =========================================================

    print(
        "\n========== CONVERSATION DEBUG =========="
    )

    print(
        "Message:",
        message,
    )

    print(
        "Previous Intent:",
        state.get("intent"),
    )

    print(
        "Symptoms:",
        state.get("symptoms"),
    )

    print(
        "Age:",
        state.get("age"),
    )

    print(
        "Missing Information:",
        state.get("missing_information"),
    )

    print(
        "Next Question:",
        state.get("next_question"),
    )

    print(
        "========================================"
    )

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

    normalized_message = normalize_text(
        message
    )

    print(
        "[DETERMINISTIC DEBUG]",
        {
            "message": message,
            "intent": detected_intent,
            "confidence": detected_confidence,
            "age": extract_age(
                normalized_message
            ),
            "symptoms": extract_symptoms(
                normalized_message
            ),
            "duration": extract_duration(
                normalized_message
            ),
            "severity": extract_severity(
                normalized_message
            ),
        }
    )

    print(
        "[DETERMINISTIC]",
        detected_intent,
        detected_confidence,
    )

    # =========================================================
    # PROFILE
    #
    # IMPORTANT:
    # Profile requests must NOT enter medical extraction.
    # They must NOT be handled by RAG.
    #
    # The actual profile lookup will be handled by
    # the application/profile service layer.
    # =========================================================

    if detected_intent == "PROFILE":

        print(
            "[ROUTING] Deterministic PROFILE -> PROFILE"
        )

        return {
            **state,
            "conversation_history": history,
            "intent": "PROFILE",
            "intent_confidence": detected_confidence,
            "assistant_response": None,
        }

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
    # Active Triage
    #
    # IMPORTANT:
    # Do NOT call Intent LLM here.
    #
    # Example:
    #
    # System:
    # "How old are you?"
    #
    # User:
    # "29"
    #
    # This must remain TRIAGE.
    # =========================================================

    if _is_active_triage(state):

        print(
            "[ROUTING] Active triage -> TRIAGE"
        )

        return {
            **state,
            "conversation_history": history,
            "intent": "TRIAGE",
            "intent_confidence": 1.0,
            "assistant_response": None,
        }

    # =========================================================
    # Deterministic TRIAGE
    #
    # Medical information was explicitly detected.
    #
    # Do NOT waste an Intent LLM call.
    # =========================================================

    if detected_intent == "TRIAGE":

        print(
            "[ROUTING] Deterministic medical detection -> TRIAGE"
        )

        intent = "TRIAGE"
        confidence = detected_confidence

    else:

        # =====================================================
        # Deterministic GENERAL
        # =====================================================

        print(
            "[ROUTING] Deterministic GENERAL -> GENERAL"
        )

        return {
            **state,
            "conversation_history": history,
            "intent": "GENERAL",
            "intent_confidence": detected_confidence,
            "assistant_response": None,
        }

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

    print(
        "[ROUTING] Starting medical extraction..."
    )

    start_time = time.perf_counter()

    extraction_result = llm_service.generate_structured(
        prompt=f"""
Extract medical information from:

{message}
""",
        response_model=ConversationExtraction,
        system_prompt=EXTRACTION_SYSTEM_PROMPT,
    )

    extraction_latency = (
        time.perf_counter()
        - start_time
    )

    print(
        f"[LATENCY] Extraction LLM: "
        f"{extraction_latency:.2f}s"
    )

    # =========================================================
    # Contract Validation
    # =========================================================

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

        age = state.get(
            "age"
        )

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
                state.get(
                    "red_flags"
                )
                or []
            )
            +
            list(
                extraction_result.red_flags
                or []
            )
        )
    )

    # =========================================================
    # Final State
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