from unittest.mock import Mock

from workflow.triage_graph import build_triage_graph


def test_llm_state_is_preserved_between_risk_and_supervisor():

    # -------------------------------------------------
    # Mock LLM Service
    # -------------------------------------------------

    llm_service = Mock()

    # Symptom extraction result
    llm_service.extract_symptoms.return_value = Mock(
        symptoms=[],
        age=None,
        duration=None,
        severity=None,
    )

    # Risk assessment result
    llm_service.generate_structured.return_value = Mock(
        risk_level="LOW",
        confidence=0.80,
        red_flags=[],
        recommendation="Monitor for worsening symptoms.",
    )

    # -------------------------------------------------
    # Build graph
    # -------------------------------------------------

    graph = build_triage_graph(
        llm_service=llm_service,
    )

    # -------------------------------------------------
    # Initial state
    # -------------------------------------------------

    state = {
        "patient_id": 2,
        "user_message": "من 35 ساله هستم، تب و سردرد شدید دارم، مدت 2 روز است",
        "conversation_history": [],
        "symptoms": [],
        "age": None,
        "duration": None,
        "severity": None,
        "missing_information": [],
    }

    # -------------------------------------------------
    # Invoke graph
    # -------------------------------------------------

    result = graph.invoke(state)

    # -------------------------------------------------
    # Verify LLM state survived Risk Agent
    # -------------------------------------------------

    assert result["llm_risk_level"] == "LOW"
    assert result["llm_confidence"] == 0.80
    assert result["llm_red_flags"] == []
    assert result["llm_recommendation"] == (
        "Monitor for worsening symptoms."
    )

    # -------------------------------------------------
    # Verify Rule-based result is still preserved
    # -------------------------------------------------

    assert result["risk_level"] == "HIGH"
    assert result["confidence"] == 0.75

    # -------------------------------------------------
    # Rule vs LLM disagreement
    # -------------------------------------------------

    assert result["supervisor_status"] == "REVIEW_REQUIRED"