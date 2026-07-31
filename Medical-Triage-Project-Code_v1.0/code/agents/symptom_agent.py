import re

from utils.text_normalizer import normalize_text
from utils.answer_parser import (
    extract_duration,
    extract_severity,
)


SYMPTOM_PATTERNS = {

    "chest pain": [
        "chest pain",
        "chest hurts",
        "pain in my chest",
        "درد قفسه سینه",
        "درد سینه",
        "قفسه سینم درد میکنه",
        "قفسه سینم درد می کنه",
    ],

    "shortness of breath": [
        "shortness of breath",
        "difficulty breathing",
        "hard to breathe",
        "تنگی نفس",
        "نفس تنگی",
        "سخت نفس میکشم",
        "سخت نفس می کشم",
    ],

    "headache": [
        "headache",
        "my head hurts",
        "سردرد",
        "سرم درد میکنه",
        "سرم درد می کنه",
        "درد سر",
    ],

    "fever": [
        "fever",
        "high temperature",
        "تب",
        "تب دارم",
    ],

    "dizziness": [
        "dizziness",
        "dizzy",
        "سرگیجه",
        "سرم گیج میره",
        "سرم گیج می رود",
    ],
}


def extract_symptoms(text):

    symptoms = []

    for symptom, patterns in SYMPTOM_PATTERNS.items():

        if any(pattern in text for pattern in patterns):
            symptoms.append(symptom)

    return symptoms


def extract_age(text):

    patterns = [
        r"\b(?:i'm|im|i am)\s+(\d{1,3})\b",
        r"\b(\d{1,3})\s*(?:years?\s*old|yo)\b",
        r"\b(\d{1,3})\s*ساله\b",
        r"\bسنم\s*(?:\s*حدود\s*)?(\d{1,3})\b",
        r"\b(\d{1,3})\s*سال\s*دارم\b",
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return int(match.group(1))

    return None

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