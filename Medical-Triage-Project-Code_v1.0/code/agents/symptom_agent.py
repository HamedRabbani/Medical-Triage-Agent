from extractors.age_extractor import extract_age
from extractors.symptom_extractor import extract_symptoms
from extractors.duration_extractor import extract_duration
from extractors.severity_extractor import extract_severity

from utils.text_normalizer import normalize_text


def symptom_agent(state):
    """Extract patient information from conversation history."""

    old_symptoms = state.get("symptoms", [])
    age = state.get("age")
    duration = state.get("duration")
    severity = state.get("severity")

    conversation_history = state.get(
        "conversation_history",
        [],
    )

    # Build patient conversation context.
    patient_messages = [
        message.get("content", "")
        for message in conversation_history
        if message.get("sender_type") == "Patient"
    ]

    # Fallback to current message.
    if not patient_messages:
        current_message = state.get(
            "user_message",
            "",
        )

        if current_message:
            patient_messages = [current_message]

    # Extract information chronologically.
    for message in patient_messages:

        text = normalize_text(message)

        # Extract symptoms
        new_symptoms = extract_symptoms(text)

        old_symptoms.extend(new_symptoms)

        # Extract age
        new_age = extract_age(text)

        if new_age is not None:
            age = new_age

        # Extract duration
        new_duration = extract_duration(text)

        if new_duration is not None:
            duration = new_duration

        # Extract severity
        new_severity = extract_severity(text)

        if new_severity is not None:
            severity = new_severity

    # Remove duplicate symptoms while preserving order.
    symptoms = list(
        dict.fromkeys(old_symptoms)
    )

    return {
        **state,
        "symptoms": symptoms,
        "age": age,
        "duration": duration,
        "severity": severity,
    }