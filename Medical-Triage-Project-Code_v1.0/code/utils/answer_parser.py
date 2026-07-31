import re


NUMBER_WORDS = {
    "one": 1,
    "a": 1,
    "یک": 1,
    "two": 2,
    "دو": 2,
    "three": 3,
    "سه": 3,
    "four": 4,
    "چهار": 4,
    "five": 5,
    "پنج": 5,
    "six": 6,
    "شش": 6,
    "seven": 7,
    "هفت": 7,
}


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


def extract_severity(text: str):

    severe = [
        "severe",
        "very severe",
        "very painful",
        "terrible",
        "a lot",
        "شدید",
        "خیلی شدید",
        "خیلی زیاده",
        "خیلی درد دارم",
        "دردم شدیده",
    ]

    moderate = [
        "moderate",
        "medium",
        "متوسط",
        "معمولی",
        "نه کم نه زیاد",
    ]

    mild = [
        "mild",
        "slight",
        "a little",
        "خفیف",
        "کم",
        "یه کم",
        "کمی",
    ]

    if any(x in text for x in severe):
        return "severe"

    if any(x in text for x in moderate):
        return "moderate"

    if any(x in text for x in mild):
        return "mild"

    return None