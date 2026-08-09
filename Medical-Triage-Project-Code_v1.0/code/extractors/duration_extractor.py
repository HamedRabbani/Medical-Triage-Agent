import re
def extract_duration(text: str):

    text = text.lower()

    patterns = [
        r"(\d+)\s*(minutes?|hours?|days?|weeks?|ماه|روز|ساعت|دقیقه|هفته)",
        r"(one|a)\s*(minute|hour|day|week)",
        r"(یک|دو|سه|چهار|پنج)\s*(روز|هفته|ساعت|دقیقه)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return match.group(0)

    if "از سه روز پیش" in text or "سه روزه" in text:
        return "3 days"

    if "دو روزه" in text:
        return "2 days"

    if "یک هفته" in text:
        return "1 week"

    if "سه روز" in text:
        return "3 days"

    return None
