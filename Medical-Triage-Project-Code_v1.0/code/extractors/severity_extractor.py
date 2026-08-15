import re


def extract_severity(text: str) -> str | None:
    """
    Extract symptom severity from text.

    The extractor avoids substring false positives.
    For example:

        "کمک می‌کنی؟"

    must NOT be interpreted as:

        severity = mild

    because "کم" is part of the word "کمک".
    """

    if not isinstance(text, str):
        return None

    text = text.strip().lower()

    # =========================================================
    # Severe
    # =========================================================

    severe_phrases = [
        "very severe",
        "very painful",
        "خیلی زیاد است",
        "خیلی زیاد",
        "خیلی زیاده",
        "خیلی شدید",
        "خیلی درد دارم",
        "دردم شدیده",
        "severe",
        "terrible",
        "شدید",
        "a lot",
        "زیاد",
        "زیاده",
    ]

    for phrase in severe_phrases:
        if phrase in text:
            return "severe"

    # =========================================================
    # Moderate
    # =========================================================

    moderate_phrases = [
        "نه کم نه زیاد",
        "moderate",
        "medium",
        "متوسط",
        "معمولی",
    ]

    for phrase in moderate_phrases:
        if phrase in text:
            return "moderate"

    # =========================================================
    # Mild
    # =========================================================

    mild_phrases = [
        "a little",
        "slight",
        "mild",
        "یه کم",
        "کمی",
        "خفیف",
        "کم درد",
        "درد کم",
        "درد کمی",
    ]

    for phrase in mild_phrases:
        if phrase in text:
            return "mild"

    # =========================================================
    # Exact Persian word "کم"
    # =========================================================
    #
    # Do NOT use:
    #
    #     "کم" in text
    #
    # because it matches:
    #
    #     کمک
    #     کمکی
    #
    # =========================================================

    if re.search(r"(?<!\S)کم(?!\S)", text):
        return "mild"

    # =========================================================
    # English exact word
    # =========================================================

    if re.search(r"\bmild\b", text):
        return "mild"

    return None