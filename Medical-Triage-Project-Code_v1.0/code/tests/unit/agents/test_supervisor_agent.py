from agents.supervisor_agent import supervisor_agent


def test_supervisor_rejects_when_rule_and_llm_disagree():

    state = {
        "risk_level": "HIGH",
        "confidence": 0.75,
        "red_flags": [],

        "llm_risk_level": "LOW",
        "llm_confidence": 0.80,
        "llm_red_flags": [],
        "llm_recommendation": "Monitor for worsening symptoms.",
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "REVIEW_REQUIRED"


def test_supervisor_rejects_when_llm_assessment_is_missing():

    state = {
        "risk_level": "HIGH",
        "confidence": 0.75,
        "red_flags": [],

        "llm_risk_level": None,
        "llm_confidence": None,
        "llm_red_flags": [],
        "llm_recommendation": None,
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "REVIEW_REQUIRED"


def test_supervisor_rejects_red_flag_disagreement():

    state = {
        "risk_level": "LOW",
        "confidence": 0.90,
        "red_flags": [],

        "llm_risk_level": "LOW",
        "llm_confidence": 0.85,
        "llm_red_flags": ["severe symptoms"],
        "llm_recommendation": "Monitor for worsening symptoms.",
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "REVIEW_REQUIRED"


def test_supervisor_rejects_high_risk_without_red_flags():

    state = {
        "risk_level": "HIGH",
        "confidence": 0.75,
        "red_flags": [],

        "llm_risk_level": "HIGH",
        "llm_confidence": 0.85,
        "llm_red_flags": [],
        "llm_recommendation": "Prompt medical evaluation is recommended.",
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "REVIEW_REQUIRED"


def test_supervisor_approves_matching_assessments_with_red_flags():

    state = {
        "risk_level": "HIGH",
        "confidence": 0.90,
        "red_flags": ["loss_of_consciousness"],

        "llm_risk_level": "HIGH",
        "llm_confidence": 0.92,
        "llm_red_flags": ["loss_of_consciousness"],
        "llm_recommendation": "Immediate medical evaluation is recommended.",
    }

    result = supervisor_agent(state)

    assert result["supervisor_status"] == "APPROVED"