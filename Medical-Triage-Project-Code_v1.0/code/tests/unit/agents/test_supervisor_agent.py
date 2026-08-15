from agents.supervisor_agent import supervisor_agent


def test_supervisor_approves_matching_low_risk():
    state = {
        "risk_level": "LOW",
        "confidence": 0.60,
        "red_flags": [],
        "llm_risk_level": "LOW",
        "llm_confidence": 0.90,
        "llm_red_flags": [],
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "APPROVED"


def test_supervisor_approves_matching_high_risk_with_red_flags():
    state = {
        "risk_level": "HIGH",
        "confidence": 0.85,
        "red_flags": [
            "chest pain with shortness of breath"
        ],
        "llm_risk_level": "HIGH",
        "llm_confidence": 1.0,
        "llm_red_flags": [
            "chest pain with shortness of breath"
        ],
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "APPROVED"


def test_supervisor_requires_review_on_risk_disagreement():
    state = {
        "risk_level": "HIGH",
        "confidence": 0.85,
        "red_flags": [
            "chest pain with shortness of breath"
        ],
        "llm_risk_level": "LOW",
        "llm_confidence": 0.90,
        "llm_red_flags": [],
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "REVIEW_REQUIRED"


def test_supervisor_requires_review_on_red_flag_disagreement():
    state = {
        "risk_level": "HIGH",
        "confidence": 0.85,
        "red_flags": [
            "chest pain with shortness of breath"
        ],
        "llm_risk_level": "HIGH",
        "llm_confidence": 0.90,
        "llm_red_flags": [],
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "REVIEW_REQUIRED"


def test_supervisor_requires_review_when_llm_assessment_missing():
    state = {
        "risk_level": "LOW",
        "confidence": 0.60,
        "red_flags": [],
        "llm_risk_level": None,
        "llm_confidence": None,
        "llm_red_flags": [],
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "REVIEW_REQUIRED"


def test_supervisor_rejects_missing_rule_assessment():
    state = {
        "risk_level": None,
        "confidence": None,
        "red_flags": [],
        "llm_risk_level": "LOW",
        "llm_confidence": 0.90,
        "llm_red_flags": [],
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "REJECTED"


def test_supervisor_requires_review_for_high_risk_without_red_flags():
    state = {
        "risk_level": "HIGH",
        "confidence": 0.75,
        "red_flags": [],
        "llm_risk_level": "HIGH",
        "llm_confidence": 0.90,
        "llm_red_flags": [],
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "REVIEW_REQUIRED"