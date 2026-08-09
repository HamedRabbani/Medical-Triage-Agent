import re
from extractors.age_extractor import extract_age
from extractors.symptom_extractor import extract_symptoms
from extractors.duration_extractor import extract_duration
from extractors.severity_extractor import extract_severity

from utils.text_normalizer import normalize_text



def symptom_agent(state):

    text = normalize_text(
        state.get("user_message", "")
    )

    old_symptoms = state.get("symptoms", [])

    new_symptoms = extract_symptoms(text)

    symptoms = list(
        dict.fromkeys(
            old_symptoms + new_symptoms
        )
    )

    old_age = state.get("age")
    new_age = extract_age(text)

    age = new_age if new_age is not None else old_age

    old_duration = state.get("duration")
    new_duration = extract_duration(text)

    duration = (
        new_duration
        if new_duration is not None
        else old_duration
    )

    old_severity = state.get("severity")
    new_severity = extract_severity(text)

    severity = (
        new_severity
        if new_severity is not None
        else old_severity
    )

    return {
        **state,
        "symptoms": symptoms,
        "age": age,
        "duration": duration,
        "severity": severity,
    }