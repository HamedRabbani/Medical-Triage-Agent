
import re

from utils.text_normalizer import normalize_text


PERSIAN_NUMBERS = {
    "یک": 1,
    "دو": 2,
    "سه": 3,
    "چهار": 4,
    "پنج": 5,
    "شش": 6,
    "هفت": 7,
    "هشت": 8,
    "نه": 9,
    "ده": 10,
}


def extract_duration(text: str) -> str | None:
    """
    Extract symptom duration explicitly stated
    in the current user message.

    The extractor does not infer duration from
    previous patients or external medical knowledge.
    """

    if not isinstance(text, str):
        return None

    text = normalize_text(text)

    if not text:
        return None

    # ---------------------------------------------------------
    # Numeric duration
    # ---------------------------------------------------------

    pattern = (
        r"(\d+)\s*"
        r"(minutes?|hours?|days?|weeks?|months?|"
        r"دقیقه|ساعت|روز|هفته|ماه)"
    )

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    )

    if match:
        return match.group(0)

    # ---------------------------------------------------------
    # English textual duration
    # ---------------------------------------------------------

    english_patterns = {
        "one minute": "1 minute",
        "one hour": "1 hour",
        "one day": "1 day",
        "one week": "1 week",
        "a minute": "1 minute",
        "an hour": "1 hour",
        "a day": "1 day",
        "a week": "1 week",
    }

    for phrase, value in english_patterns.items():

        if phrase in text:
            return value

    # ---------------------------------------------------------
    # Persian textual numbers
    # ---------------------------------------------------------

    for word, number in PERSIAN_NUMBERS.items():

        pattern = (
            rf"{word}\s*"
            rf"(روز|هفته|ساعت|دقیقه|ماه)"
        )

        match = re.search(
            pattern,
            text,
        )

        if match:

            unit = match.group(1)

            return f"{number} {unit}"

    return None

