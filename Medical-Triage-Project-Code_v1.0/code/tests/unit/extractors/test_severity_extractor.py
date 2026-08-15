from extractors.severity_extractor import extract_severity


def test_help_word_is_not_mild():
    result = extract_severity(
        "میتونی کمکم کنی؟"
    )

    assert result is None


def test_mild_pain():
    result = extract_severity(
        "درد کم دارم"
    )

    assert result == "mild"


def test_persian_kami():
    result = extract_severity(
        "درد کمی دارم"
    )

    assert result == "mild"


def test_severe_pain():
    result = extract_severity(
        "دردم خیلی شدیده"
    )

    assert result == "severe"


def test_moderate_pain():
    result = extract_severity(
        "درد متوسط دارم"
    )

    assert result == "moderate"