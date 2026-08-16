import re

from utils.text_normalizer import normalize_text


SEVERITY_PATTERNS = {
    "severe": [
        r"\bsevere\b",
        r"\bvery\s+severe\b",
        r"\bvery\s+painful\b",
        r"\bterrible\b",
        r"\ba\s+lot\b",

        r"(?<![\w\u0600-\u06FF])شدید(?![\w\u0600-\u06FF])",
        r"خیلی\s+شدید",
        r"خیلی\s+زیاده",
        r"خیلی\s+زیاد(?:\s+است)?",
        r"خیلی\s+درد\s+دارم",
        r"دردم\s+شدیده",
        r"(?<![\w\u0600-\u06FF])زیاد(?![\w\u0600-\u06FF])",
    ],

    "moderate": [
        r"\bmoderate\b",
        r"\bmedium\b",

        r"(?<![\w\u0600-\u06FF])متوسط(?![\w\u0600-\u06FF])",
        r"(?<![\w\u0600-\u06FF])معمولی(?![\w\u0600-\u06FF])",
        r"نه\s+کم\s+نه\s+زیاد",
    ],

    "mild": [
        r"\bmild\b",
        r"\bslight\b",
        r"\ba\s+little\b",

        r"(?<![\w\u0600-\u06FF])خفیف(?![\w\u0600-\u06FF])",
        r"(?<![\w\u0600-\u06FF])کم(?![\w\u0600-\u06FF])",
        r"یه\s+کم",
        r"(?<![\w\u0600-\u06FF])کمی(?![\w\u0600-\u06FF])",
    ],
}


def extract_severity(text):

    if not isinstance(
        text,
        str,
    ):
        return None

    text = normalize_text(
        text
    )

    if not text:
        return None

    # =========================================================
    # Moderate
    # =========================================================

    for pattern in SEVERITY_PATTERNS["moderate"]:

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            return "moderate"

    # =========================================================
    # Severe
    # =========================================================

    for pattern in SEVERITY_PATTERNS["severe"]:

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            return "severe"

    # =========================================================
    # Mild
    # =========================================================

    for pattern in SEVERITY_PATTERNS["mild"]:

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            return "mild"

    return None