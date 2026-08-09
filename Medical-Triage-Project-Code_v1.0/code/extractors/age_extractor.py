import re

def extract_age(text):

    patterns = [
        r"\b(?:i'm|im|i am)\s+(\d{1,3})\b",
        r"\b(\d{1,3})\s*(?:years?\s*old|yo)\b",
        r"\b(\d{1,3})\s*ساله\b",
        r"\bسنم\s*(?:\s*حدود\s*)?(\d{1,3})\b",
        r"\b(\d{1,3})\s*سال\s*دارم\b",
        r"^(\d{1,3})$",
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return int(match.group(1))

    return None