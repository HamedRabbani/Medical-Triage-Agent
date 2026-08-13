from agents.planner_agent import planner_agent


def test_planner_with_complete_data() -> None:
    """Planner should not ask a question when data is complete."""

    state = {
        "age": 29,
        "symptoms": ["chest pain"],
        "duration": "20 minutes",
        "severity": "severe",
    }

    result = planner_agent(state)

    print("\n=== Complete Data Test ===")
    print(f"Missing: {result.get('missing_information')}")
    print(f"Question: {result.get('next_question')}")

    assert result["missing_information"] == []
    assert result["next_question"] is None


def test_planner_with_missing_age() -> None:
    """Planner should ask for age when age is missing."""

    state = {
        "age": None,
        "symptoms": ["chest pain"],
        "duration": "20 minutes",
        "severity": "severe",
    }

    result = planner_agent(state)

    print("\n=== Missing Age Test ===")
    print(f"Missing: {result.get('missing_information')}")
    print(f"Question: {result.get('next_question')}")

    assert result["missing_information"] == ["age"]
    assert result["next_question"] == (
        "How old are you? / چند سال دارید؟"
    )


def test_planner_with_missing_severity() -> None:
    """Planner should ask for severity when severity is missing."""

    state = {
        "age": 29,
        "symptoms": ["chest pain"],
        "duration": "20 minutes",
        "severity": None,
    }

    result = planner_agent(state)

    print("\n=== Missing Severity Test ===")
    print(f"Missing: {result.get('missing_information')}")
    print(f"Question: {result.get('next_question')}")

    assert result["missing_information"] == ["severity"]
    assert result["next_question"] == (
        "How severe are your symptoms? / شدت علائم چقدر است؟"
    )


if __name__ == "__main__":
    test_planner_with_complete_data()
    test_planner_with_missing_age()
    test_planner_with_missing_severity()

    print("\nAll planner tests PASSED.")