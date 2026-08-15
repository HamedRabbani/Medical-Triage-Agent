from extractors.age_extractor import extract_age
from extractors.symptom_extractor import extract_symptoms
from extractors.duration_extractor import extract_duration
from extractors.severity_extractor import extract_severity

from utils.text_normalizer import normalize_text


def symptom_agent(state, llm_service=None):
    """
    Extract patient information from the current conversation.

    Deterministic extractors are the baseline.
    LLM extraction is optional and must never destroy
    already extracted information.
    """

    symptoms = list(state.get("symptoms") or [])

    age = state.get("age")
    duration = state.get("duration")
    severity = state.get("severity")

    # ---------------------------------------------------------
    # Collect patient messages
    # ---------------------------------------------------------

    conversation_history = (
        state.get("conversation_history") or []
    )

    patient_messages = []

    for message in conversation_history:
        if not isinstance(message, dict):
            continue

        if message.get("sender_type") == "Patient":
            content = message.get("content")

            if isinstance(content, str) and content.strip():
                patient_messages.append(content)

    # ---------------------------------------------------------
    # Fallback to current user message
    # ---------------------------------------------------------

    current_message = state.get(
        "user_message",
        "",
    )

    if (
        isinstance(current_message, str)
        and current_message.strip()
        and current_message not in patient_messages
    ):
        patient_messages.append(current_message)

    # ---------------------------------------------------------
    # Deterministic extraction
    # ---------------------------------------------------------

    for message in patient_messages:

        text = normalize_text(message)

        # Symptoms
        extracted_symptoms = extract_symptoms(text)

        for symptom in extracted_symptoms:
            if symptom not in symptoms:
                symptoms.append(symptom)

        # Age
        extracted_age = extract_age(text)

        if extracted_age is not None:
            age = extracted_age

        # Duration
        extracted_duration = extract_duration(text)

        if extracted_duration is not None:
            duration = extracted_duration

        # Severity
        extracted_severity = extract_severity(text)

        if extracted_severity is not None:
            severity = extracted_severity

    # ---------------------------------------------------------
    # LLM extraction
    # ---------------------------------------------------------
    #
    # Do NOT call a second LLM extraction here when the
    # Conversation Agent has already extracted structured
    # information.
    #
    # This prevents:
    #
    # Conversation Agent
    #       ↓
    # extraction
    #       ↓
    # Symptom Agent
    #       ↓
    # second extraction
    #
    # and makes Mock call ordering deterministic.
    # ---------------------------------------------------------

    return {
        **state,
        "symptoms": list(dict.fromkeys(symptoms)),
        "age": age,
        "duration": duration,
        "severity": severity,
    }