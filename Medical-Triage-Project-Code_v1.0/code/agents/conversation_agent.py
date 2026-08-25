import time
import re

from application.contracts.conversation_extraction import (
    ConversationExtraction,
)

from application.contracts.short_term_memory import (
    ShortTermMemory,
)

from application.services.short_term_memory_service import (
    ShortTermMemoryService,
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

Extract the following fields when explicitly present:

- symptoms
- severity
- age
- duration
- pain_location
- red_flags

For pain_location:

- Extract the anatomical location of pain only when
  the user explicitly states it.
- Examples:
  "درد شکمم" -> pain_location = "abdomen"
  "سردرد دارم" -> pain_location = "head"
  "کمرم درد می‌کند" -> pain_location = "back"
  "درد قفسه سینه دارم" -> pain_location = "chest"
- If the user only says "درد دارم", do NOT invent a location.
  Return pain_location = null.

Return structured output only.
"""


# =============================================================
# Active Triage Detection
# =============================================================

def _is_active_triage(state):
    """
    Determine whether the system is already inside
    an active medical triage flow.
    """

    if state.get(
        "missing_information"
    ):

        return True

    if state.get(
        "next_question"
    ) is not None:

        return True

    return False


# =============================================================
# Profile Intent Detection
# =============================================================

def _is_profile_request(
    text: str,
) -> bool:
    """
    Detect whether the user is asking about
    their own profile/account information.
    """

    profile_keywords = [

        # -----------------------------------------------------
        # Persian
        # -----------------------------------------------------

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
        "مشخصات خودم",

        "سنم",
        "سن من",

        "نقشم",
        "نقش من",

        "حساب من",

        # -----------------------------------------------------
        # English
        # -----------------------------------------------------

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

    1. PROFILE request
    2. Active triage context
    3. Explicit medical information
    4. GENERAL
    """

    text = normalize_text(
        message
    )

    if not text:

        return (
            "GENERAL",
            0.9,
        )

    # =========================================================
    # Profile
    # =========================================================

    if _is_profile_request(
        text
    ):

        return (
            "PROFILE",
            1.0,
        )

    # =========================================================
    # Existing active triage
    # =========================================================

    if _is_active_triage(
        state
    ):

        return (
            "TRIAGE",
            1.0,
        )

    # =========================================================
    # Symptom detection
    # =========================================================

    symptoms = extract_symptoms(
        text
    )

    if symptoms:

        return (
            "TRIAGE",
            1.0,
        )

    # =========================================================
    # Age detection
    # =========================================================
    age = extract_age(
        text
    )

    if age is not None:

        return (
            "TRIAGE",
            0.9,
        )

    # =========================================================
    # Duration detection
    # =========================================================

    duration = extract_duration(
        text
    )

    if duration is not None:

        return (
            "TRIAGE",
            0.9,
        )

    # =========================================================
    # Severity detection
    # =========================================================

    severity = extract_severity(
        text
    )

    if severity is not None:

        return (
            "TRIAGE",
            0.9,
        )

    # =========================================================
    # General
    # =========================================================

    return (
        "GENERAL",
        0.9,
    )


# =============================================================
# Pain Location Mapping
# =============================================================

def _infer_pain_location_from_symptoms(
    symptoms: list[str],
) -> str | None:
    """
    Infer pain location only from an already-detected
    canonical symptom.

    This is deterministic and does not invent a location
    for generic pain.
    """

    location_map = {

        "chest pain": "chest",

        "abdominal pain": "abdomen",

        "back pain": "back",

        "neck pain": "neck",

        "leg pain": "leg",

        "headache": "head",
    }

    for symptom in symptoms:

        location = location_map.get(
            symptom
        )

        if location:

            return location

    return None


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

        message = str(
            message
        )

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
        "Pain Location:",
        state.get("pain_location"),
    )

    print(
        "Missing Information:",
        state.get(
            "missing_information"
        ),
    )

    print(
        "Next Question:",
        state.get(
            "next_question"
        ),
    )

    print(
        "========================================"
    )

    # =========================================================
    # Conversation History
    #
    # IMPORTANT:
    #
    # session_agent already persists the current message
    # and reloads conversation history from the database.
    #
    # Therefore DO NOT append the current message again.
    # =========================================================

    history = list(
        state.get(
            "conversation_history"
        )
        or []
    )

    # =========================================================
    # Deterministic Baseline
    # =========================================================

    (
        detected_intent,
        detected_confidence,
    ) = _detect_intent_from_message(
        state,
        message,
    )

    normalized_message = normalize_text(
        message
    )

    detected_age = extract_age(
        normalized_message
    )

    detected_symptoms = extract_symptoms(
        normalized_message
    )

    detected_duration = extract_duration(
        normalized_message
    )

    detected_severity = extract_severity(
        normalized_message
    )

    deterministic_pain_location = (
        _infer_pain_location_from_symptoms(
            detected_symptoms
        )
    )

    print(
        "[DETERMINISTIC DEBUG]",
        {
            "message": message,
            "intent": detected_intent,
            "confidence": detected_confidence,
            "age": detected_age,
            "symptoms": detected_symptoms,
            "duration": detected_duration,
            "severity": detected_severity,
            "pain_location": (
                deterministic_pain_location
            ),
        },
    )

    print(
        "[DETERMINISTIC]",
        detected_intent,
        detected_confidence,
    )

    # =========================================================
    # PROFILE
    # =========================================================

    if detected_intent == "PROFILE":

        print(
            "[ROUTING] Deterministic PROFILE -> PROFILE"
        )

        return {
            **state,

            "conversation_history": history,

            "intent": "PROFILE",

            "intent_confidence": (
                detected_confidence
            ),

            "assistant_response": None,

            "response": None,
        }

    # =========================================================
    # No LLM
    # =========================================================

    if llm_service is None:

        return {
            **state,

            "conversation_history": history,

            "intent": detected_intent,

            "intent_confidence": (
                detected_confidence
            ),

            "assistant_response": None,

            "response": None,
        }

    # =========================================================
    # Intent Resolution
    # =========================================================

    if _is_active_triage(
        state
    ):

        print(
            "[ROUTING] Active triage -> TRIAGE"
        )

        intent = "TRIAGE"

        confidence = 1.0

    elif detected_intent == "TRIAGE":

        print(
            "[ROUTING] Deterministic medical detection -> TRIAGE"
        )

        intent = "TRIAGE"

        confidence = (
            detected_confidence
        )

    else:

        print(
            "[ROUTING] Deterministic GENERAL -> GENERAL"
        )

        return {
            **state,

            "conversation_history": history,

            "intent": "GENERAL",

            "intent_confidence": (
                detected_confidence
            ),

            "assistant_response": None,

            "response": None,
        }

    # =========================================================
    # TRIAGE Extraction
    # =========================================================

    print(
        "[ROUTING] Starting medical extraction..."
    )

    start_time = time.perf_counter()

    extraction_result = (
        llm_service.generate_structured(
            prompt=f"""
Extract medical information from this user's message:

{message}
""",
            response_model=ConversationExtraction,
            system_prompt=EXTRACTION_SYSTEM_PROMPT,
        )
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
    # Deterministic Safety / Consistency
    #
    # If the LLM failed to identify a specific location,
    # use our deterministic symptom mapping.
    # =========================================================

    extracted_pain_location = (
        extraction_result.pain_location
    )

    if (
        extracted_pain_location is None
        and deterministic_pain_location is not None
    ):

        extracted_pain_location = (
            deterministic_pain_location
        )

    # =========================================================
    # Preserve Previous Pain Location
    # =========================================================

    previous_pain_location = state.get(
        "pain_location"
    )

    if (
        extracted_pain_location is None
        and previous_pain_location is not None
    ):

        extracted_pain_location = (
            previous_pain_location
        )

    # =========================================================
    # Memory Update
    # =========================================================

    memory = state.get(
        "short_term_memory"
    )

    if memory is None:

        memory = ShortTermMemory(
            session_id=state.get(
                "session_id"
            ),
        )

    # =========================================================
    # Make sure the extraction contains the
    # deterministic pain location.
    # =========================================================

    extraction_result = (
        extraction_result.model_copy(
            update={
                "pain_location": (
                    extracted_pain_location
                ),
            }
        )
    )

    memory_service = (
        ShortTermMemoryService()
    )

    memory = memory_service.update(
        memory=memory,
        extraction=extraction_result,
    )

    # =========================================================
    # Final State
    # =========================================================

    medical_context = (
        memory.medical_context
    )

    return {
        **state,

        "conversation_history": history,

        "short_term_memory": memory,

        "intent": intent,

        "intent_confidence": confidence,

        "symptoms": (
            medical_context.symptoms
        ),

        "age": (
            medical_context.age
        ),

        "duration": (
            medical_context.duration
        ),

        "severity": (
            medical_context.severity
        ),

        "pain_location": (
            medical_context.pain_location
        ),

        "red_flags": (
            medical_context.red_flags
        ),

        "assistant_response": None,

        "response": None,
    }