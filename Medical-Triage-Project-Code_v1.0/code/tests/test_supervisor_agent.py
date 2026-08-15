from agents.supervisor_agent import supervisor_agent


def test_supervisor_approved() -> None:
    state = {
        "risk_level": "LOW",
        "confidence": 0.90,
        "red_flags": [],
        "llm_risk_level": "LOW",
        "llm_confidence": 0.90,
        "llm_red_flags": [],
    }

    result = supervisor_agent(state)

    print("\n=== Approved Test ===")
    print(f"Status: {result.get('supervisor_status')}")

    assert result["supervisor_status"] == "APPROVED"


def test_supervisor_high_with_red_flags() -> None:
    state = {
        "risk_level": "HIGH",
        "confidence": 0.90,
        "red_flags": ["chest pain"],
        "llm_risk_level": "HIGH",
        "llm_confidence": 0.90,
        "llm_red_flags": ["chest pain"],
    }

    result = supervisor_agent(state)

    print("\n=== High Risk + Red Flag Test ===")
    print(f"Status: {result.get('supervisor_status')}")

    assert result["supervisor_status"] == "APPROVED"


def test_supervisor_high_without_red_flags() -> None:
    state = {
        "risk_level": "HIGH",
        "confidence": 0.90,
        "red_flags": [],
        "llm_risk_level": "HIGH",
        "llm_confidence": 0.90,
        "llm_red_flags": [],
    }

    result = supervisor_agent(state)

    print("\n=== High Risk Without Red Flag Test ===")
    print(f"Status: {result.get('supervisor_status')}")

    assert result["supervisor_status"] == "REVIEW_REQUIRED"


def test_supervisor_missing_risk() -> None:
    state = {
        "risk_level": None,
        "confidence": 0.90,
        "red_flags": [],
        "llm_risk_level": "LOW",
        "llm_confidence": 0.90,
        "llm_red_flags": [],
    }

    result = supervisor_agent(state)

    print("\n=== Missing Risk Test ===")
    print(f"Status: {result.get('supervisor_status')}")

    assert result["supervisor_status"] == "REJECTED"