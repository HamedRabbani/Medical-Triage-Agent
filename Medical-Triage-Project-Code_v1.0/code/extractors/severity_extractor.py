def extract_severity(text: str) -> str | None:
    """Extract symptom severity from text."""

    # Check longer phrases before shorter phrases
    severe = [
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
    ]

    moderate = [
        "نه کم نه زیاد",
        "moderate",
        "medium",
        "متوسط",
        "معمولی",
    ]

    mild = [
        "a little",
        "slight",
        "mild",
        "یه کم",
        "کمی",
        "خفیف",
        "کم",
    ]

    # Check specific moderate phrases first
    if any(
        phrase in text
        for phrase in moderate
    ):
        return "moderate"

    # Check severe phrases
    if any(
        phrase in text
        for phrase in severe
    ):
        return "severe"

    # Check mild phrases
    if any(
        phrase in text
        for phrase in mild
    ):
        return "mild"

    return None