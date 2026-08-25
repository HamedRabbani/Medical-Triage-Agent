import re


def normalize_text(text: str) -> str:
    text = text.lower().strip()

    translation = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789",
    )

    text = text.translate(translation)

    text = text.replace("ی", "ی")
    text = text.replace("ي", "ی")
    text = text.replace("ى", "ی")
    text = text.replace("ک", "ک")
    text = text.replace("ك", "ک")

    text = re.sub(r"\s+", " ", text)

    return text