from extractors.symptom_extractor import extract_symptoms


def test_chest_pain():
    result = extract_symptoms(
        "درد قفسه سینه دارم"
    )

    assert "chest pain" in result


def test_shortness_of_breath():
    result = extract_symptoms(
        "تنگی نفس دارم"
    )

    assert "shortness of breath" in result


def test_multiple_symptoms():
    result = extract_symptoms(
        "درد قفسه سینه دارم و تنگی نفس"
    )

    assert "chest pain" in result
    assert "shortness of breath" in result


def test_english_chest_pain():
    result = extract_symptoms(
        "I have chest pain"
    )

    assert "chest pain" in result


def test_english_shortness_of_breath():
    result = extract_symptoms(
        "I have shortness of breath"
    )

    assert "shortness of breath" in result


def test_general_greeting_has_no_symptoms():
    result = extract_symptoms(
        "سلام، حالت چطوره؟"
    )

    assert result == []


def test_general_help_request_has_no_symptoms():
    result = extract_symptoms(
        "میتونی کمکم کنی؟"
    )

    assert result == []


def test_unrelated_message_has_no_symptoms():
    result = extract_symptoms(
        "امروز هوا خیلی خوبه"
    )

    assert result == []


def test_duplicate_symptoms_are_removed():
    result = extract_symptoms(
        "درد قفسه سینه دارم، قفسه سینه ام درد می کند"
    )

    assert result.count("chest pain") == 1


def test_chest_pressure():
    result = extract_symptoms(
        "احساس فشار روی قفسه سینه دارم"
    )

    assert "chest pressure" in result


def test_headache():
    result = extract_symptoms(
        "سردرد دارم"
    )

    assert "headache" in result


def test_abdominal_pain():
    result = extract_symptoms(
        "شکمم درد می کنه"
    )

    assert "abdominal pain" in result