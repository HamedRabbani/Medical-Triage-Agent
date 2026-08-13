import re


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
        "زیاد",
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