from extractors.severity_extractor import extract_severity


def test_severity_extractor() -> None:
    """Test severity extraction patterns."""

    test_cases = {
        # Severe
        "severe": "severe",
        "very severe": "severe",
        "very painful": "severe",
        "terrible": "severe",
        "a lot": "severe",
        "شدید": "severe",
        "خیلی شدید": "severe",
        "خیلی زیاده": "severe",
        "خیلی زیاد": "severe",
        "خیلی زیاد است": "severe",
        "خیلی درد دارم": "severe",
        "دردم شدیده": "severe",
        "زیاد": "severe",

        # Moderate
        "moderate": "moderate",
        "medium": "moderate",
        "متوسط": "moderate",
        "معمولی": "moderate",
        "نه کم نه زیاد": "moderate",

        # Mild
        "mild": "mild",
        "slight": "mild",
        "a little": "mild",
        "خفیف": "mild",
        "کم": "mild",
        "یه کم": "mild",
        "کمی": "mild",

        # Unknown
        "hello": None,
        "nothing": None,
    }

    for text, expected in test_cases.items():
        result = extract_severity(text)

        print(
            f"text={text!r} | "
            f"result={result!r} | "
            f"expected={expected!r}"
        )

        assert result == expected, (
            f"Failed for input: {text!r}"
        )


if __name__ == "__main__":
    test_severity_extractor()