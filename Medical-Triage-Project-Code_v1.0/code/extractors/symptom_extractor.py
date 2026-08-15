import re

from utils.text_normalizer import normalize_text


# =============================================================
# Symptom Patterns
# =============================================================
#
# Canonical symptom name -> possible user expressions
#
# The extractor returns canonical English names.
# The input can be Persian or English.
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
        "سرم گیج میره",
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
    # Pain
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

    # Normalize common Persian character variants.
    normalized = (
        normalized
        .replace("ي", "ی")
        .replace("ى", "ی")
        .replace("ك", "ک")
        .replace("ۀ", "ه")
        .replace("ة", "ه")
    )

    # Normalize Arabic/Persian punctuation.
    normalized = re.sub(
        r"[،؛؟]+",
        " ",
        normalized,
    )

    # Normalize English punctuation.
    normalized = re.sub(
        r"[,.!?;:]+",
        " ",
        normalized,
    )

    # Collapse multiple spaces.
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
    Safely determine whether a symptom phrase exists
    in the normalized text.

    For multi-word phrases:
        substring matching is acceptable.

    For short single words:
        word-boundary matching prevents false positives.

    Example:

        "کمک"

    must not match:

        "کم"
    """

    phrase = phrase.strip().lower()

    if not phrase:
        return False

    # ---------------------------------------------------------
    # Multi-word phrase
    # ---------------------------------------------------------

    if " " in phrase:
        return phrase in text

    # ---------------------------------------------------------
    # Single word
    # ---------------------------------------------------------

    # Persian words do not always behave perfectly with
    # Python's \b, so use whitespace-aware boundaries.
    pattern = rf"(?<!\S){re.escape(phrase)}(?!\S)"

    return re.search(pattern, text) is not None


# =============================================================
# Main Extractor
# =============================================================

def extract_symptoms(text: str) -> list[str]:
    """
    Extract canonical symptoms from user text.

    Parameters
    ----------
    text:
        User message in Persian or English.

    Returns
    -------
    list[str]
        Canonical symptom names.

    Examples
    --------
    >>> extract_symptoms("درد قفسه سینه دارم")
    ['chest pain']

    >>> extract_symptoms(
    ...     "درد قفسه سینه دارم و تنگی نفس"
    ... )
    ['chest pain', 'shortness of breath']

    >>> extract_symptoms("Hello, how are you?")
    []
    """

    if not isinstance(text, str):
        return []

    normalized_text = _normalize_for_matching(text)

    if not normalized_text:
        return []

    detected_symptoms: list[str] = []

    # =========================================================
    # Match patterns
    # =========================================================

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

                # Once a canonical symptom is found,
                # no need to check its remaining aliases.
                break

    # =========================================================
    # Remove duplicates while preserving order
    # =========================================================

    return list(
        dict.fromkeys(detected_symptoms)
    )