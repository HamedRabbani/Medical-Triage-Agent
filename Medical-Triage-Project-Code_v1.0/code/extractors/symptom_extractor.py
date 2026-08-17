
import re

from utils.text_normalizer import normalize_text


# =============================================================
# Symptom Patterns
# =============================================================
#
# Canonical symptom name -> possible user expressions
#
# The extractor only extracts information explicitly stated
# by the current user message.
#
# It does NOT:
# - access patient profiles
# - access other patients
# - access medical knowledge
# - perform risk assessment
# - use RAG
#
# =============================================================

SYMPTOM_PATTERNS: dict[str, list[str]] = {

    # ---------------------------------------------------------
    # Cardiovascular
    # ---------------------------------------------------------

    "chest pain": [
        "chest pain",
        "chest ache",
        "pain in my chest",
        "pain on my chest",

        "درد قفسه سینه",
        "درد قفسه سینه دارم",
        "درد سینه",
        "سینه درد",
        "قفسه سینم درد میکنه",
        "قفسه سینم درد می کنه",
        "قفسه سینه ام درد میکنه",
        "قفسه سینه ام درد می کنه",
        "درد در قفسه سینه",
    ],

    "chest pressure": [
        "chest pressure",
        "pressure in my chest",
        "pressure on my chest",

        "فشار روی قفسه سینه",
        "فشار روی سینه",
        "احساس فشار در قفسه سینه",
        "احساس فشار روی قفسه سینه",
    ],

    "palpitations": [
        "palpitations",
        "heart palpitations",
        "heart racing",
        "racing heart",

        "تپش قلب",
        "قلبم تند میزنه",
        "قلبم تند می زنه",
        "تند زدن قلب",
    ],

    # ---------------------------------------------------------
    # Respiratory
    # ---------------------------------------------------------

    "shortness of breath": [
        "shortness of breath",
        "difficulty breathing",
        "trouble breathing",
        "hard to breathe",
        "can't breathe",
        "cannot breathe",
        "breathing difficulty",

        "تنگی نفس",
        "تنگ نفس",
        "نفس تنگی",
        "نفس کم میارم",
        "نفس کم می آورم",
        "سخت نفس میکشم",
        "سخت نفس می کشم",
        "نمی تونم نفس بکشم",
        "نمیتونم نفس بکشم",
    ],

    "cough": [
        "cough",
        "coughing",

        "سرفه",
        "سرفه دارم",
        "سرفه میکنم",
        "سرفه می کنم",
    ],

    "wheezing": [
        "wheezing",
        "wheeze",

        "خس خس",
        "خس خس سینه",
        "خس خس میکنم",
        "خس خس می کنم",
    ],

    # ---------------------------------------------------------
    # Neurological
    # ---------------------------------------------------------

    "headache": [
        "headache",
        "head pain",

        "سر درد",
        "سردرد",
        "سرم درد میکنه",
        "سرم درد می کنه",
    ],

    "dizziness": [
        "dizziness",
        "dizzy",
        "feeling dizzy",

        "سرگیجه",
        "سرم گیج میره",
        "سرم گیج می رود",
        "احساس سرگیجه",
    ],

    "fainting": [
        "fainting",
        "fainted",
        "passed out",
        "loss of consciousness",

        "غش",
        "غش کردم",
        "بیهوش شدم",
        "از حال رفتم",
        "از هوش رفتم",
    ],

    "confusion": [
        "confusion",
        "confused",
        "mental confusion",

        "گیجی",
        "گیج هستم",
        "گیج شدم",
        "اختلال هوشیاری",
        "حواس پرتی شدید",
    ],

    # ---------------------------------------------------------
    # Gastrointestinal
    # ---------------------------------------------------------

    "abdominal pain": [
        "abdominal pain",
        "stomach pain",
        "belly pain",
        "pain in my abdomen",

        "درد شکم",
        "دل درد",
        "شکم درد",
        "درد معده",
        "معده ام درد میکنه",
        "معده ام درد می کنه",
        "شکمم درد میکنه",
        "شکمم درد می کنه",
    ],

    "nausea": [
        "nausea",
        "nauseous",
        "feeling nauseous",

        "تهوع",
        "حالت تهوع",
        "حالم تهوع داره",
        "حالت تهوع دارم",
    ],

    "vomiting": [
        "vomiting",
        "vomit",
        "throwing up",

        "استفراغ",
        "بالا آوردن",
        "بالا آوردم",
        "استفراغ کردم",
    ],

    "diarrhea": [
        "diarrhea",
        "loose stool",

        "اسهال",
        "مدفوع شل",
    ],

    # ---------------------------------------------------------
    # Musculoskeletal
    # ---------------------------------------------------------

    "back pain": [
        "back pain",
        "pain in my back",

        "درد کمر",
        "کمر درد",
        "کمرم درد میکنه",
        "کمرم درد می کنه",
    ],

    "neck pain": [
        "neck pain",
        "pain in my neck",

        "درد گردن",
        "گردن درد",
        "گردنم درد میکنه",
        "گردنم درد می کنه",
    ],

    "leg pain": [
        "leg pain",
        "pain in my leg",
        "pain in my legs",
        "my leg hurts",
        "my legs hurt",

        "درد پا",
        "پا درد",
        "پام درد میکنه",
        "پام درد می کنه",
        "پاهام درد میکنه",
        "پاهام درد می کنه",
        "پاهایم درد می کند",
        "پاهایم درد میکنه",
    ],

    "fracture": [
        "fracture",
        "broken leg",
        "my leg is broken",
        "broken my leg",

        "شکستگی",
        "پایم شکسته",
        "پام شکسته",
        "پاهام شکسته",
        "پایم شکسته است",
        "پام شکسته است",
        "پاهام شکسته است",
        "پایم شکسته شده",
        "پام شکسته شده",
    ],

    # ---------------------------------------------------------
    # General
    # ---------------------------------------------------------

    "fever": [
        "fever",
        "high temperature",

        "تب",
        "تب دارم",
        "تب کردم",
        "تب بالا",
    ],

    "fatigue": [
        "fatigue",
        "tired",
        "very tired",
        "extreme tiredness",

        "خستگی",
        "خسته ام",
        "خیلی خسته ام",
        "احساس خستگی",
    ],

    "weakness": [
        "weakness",
        "weak",
        "feeling weak",

        "ضعف",
        "ضعف دارم",
        "احساس ضعف",
        "بی حالی",
        "بی حالم",
        "بی حالی شدید",
    ],

    "swelling": [
        "swelling",
        "swollen",

        "تورم",
        "ورم",
        "ورم کرده",
        "متورم",
    ],
}


# =============================================================
# Internal Helpers
# =============================================================

def _normalize_for_matching(text: str) -> str:
    """
    Normalize user input before symptom matching.
    """

    if not isinstance(text, str):
        return ""

    normalized = normalize_text(text)

    normalized = (
        normalized
        .replace("ي", "ی")
        .replace("ى", "ی")
        .replace("ك", "ک")
        .replace("ۀ", "ه")
        .replace("ة", "ه")
    )

    normalized = re.sub(
        r"[،؛؟]+",
        " ",
        normalized,
    )

    normalized = re.sub(
        r"[,.!?;:]+",
        " ",
        normalized,
    )

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    return normalized.strip()


def _phrase_matches(
    text: str,
    phrase: str,
) -> bool:
    """
    Safely determine whether a phrase exists in text.
    """

    phrase = phrase.strip().lower()

    if not phrase:
        return False

    if " " in phrase:
        return phrase in text

    pattern = (
        rf"(?<!\S)"
        rf"{re.escape(phrase)}"
        rf"(?!\S)"
    )

    return re.search(
        pattern,
        text,
    ) is not None


# =============================================================
# Main Extractor
# =============================================================

def extract_symptoms(text: str) -> list[str]:
    """
    Extract canonical symptoms explicitly stated
    in the current user message.

    Returns canonical English symptom names.
    """

    if not isinstance(text, str):
        return []

    normalized_text = _normalize_for_matching(text)

    if not normalized_text:
        return []

    detected_symptoms: list[str] = []

    # ---------------------------------------------------------
    # Specific symptoms
    # ---------------------------------------------------------

    for symptom, patterns in SYMPTOM_PATTERNS.items():

        for pattern in patterns:

            normalized_pattern = _normalize_for_matching(
                pattern
            )

            if not normalized_pattern:
                continue

            if _phrase_matches(
                normalized_text,
                normalized_pattern,
            ):
                detected_symptoms.append(symptom)
                break

    # ---------------------------------------------------------
    # Generic pain fallback
    #
    # Only add "general pain" when no specific
    # pain location was detected.
    # ---------------------------------------------------------

    specific_pain_symptoms = {
        "chest pain",
        "abdominal pain",
        "back pain",
        "neck pain",
        "leg pain",
    }

    has_specific_pain = any(
        symptom in specific_pain_symptoms
        for symptom in detected_symptoms
    )

    if (
        not has_specific_pain
        and _phrase_matches(
            normalized_text,
            "درد",
        )
    ):
        detected_symptoms.append(
            "general pain"
        )

    return list(
        dict.fromkeys(
            detected_symptoms
        )
    )

