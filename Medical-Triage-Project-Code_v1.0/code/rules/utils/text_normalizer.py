import re


def normalize_text(text: str) -> str:
    text = text.lower().strip()

    translation = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹",
        "0123456789"
    )

    text = text.translate(translation)

    text = text.replace("ي", "ی")
    text = text.replace("ى", "ی")
    text = text.replace("ك", "ک")

    text = re.sub(r"\s+", " ", text)

    return text