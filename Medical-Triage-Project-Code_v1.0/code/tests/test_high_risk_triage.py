from workflow.triage_graph import triage_graph


def invoke_turn(
    state: dict,
    message: str,
) -> dict:
    """Run one real conversation turn."""

    current_state = {
        **state,
        "user_message": message,
    }

    return triage_graph.invoke(current_state)


def test_high_risk_triage() -> None:
    """
    Test immediate high-risk triage.

    Scenario:
        Patient reports chest pain + shortness of breath.

    Expected behavior:
        - Session is created.
        - Both symptoms are extracted.
        - Planner does not require additional information.
        - Risk assessment is performed immediately.
        - Risk level is HIGH.
        - Persistence creates a TriageResult.
    """

    # =========================================================
    # Initial State
    # =========================================================

    state = {
        "patient_id": 2,
        "session_id": None,

        "user_message": "",

        "age": None,
        "symptoms": [],
        "severity": None,
        "duration": None,

        "red_flags": [],
        "missing_information": [],
        "next_question": None,

        "risk_level": None,
        "confidence": None,
        "recommendation": None,

        "supervisor_status": None,

        "conversation_history": [],
        "result_id": None,
    }

    # =========================================================
    # Turn 1
    # =========================================================

    state = invoke_turn(
        state,
        "I have chest pain and shortness of breath.",
    )

    # =========================================================
    # Debug Output
    # =========================================================

    print("\n========================================")
    print("HIGH-RISK TRIAGE TEST")
    print("========================================")

    print(
        f"Session ID: "
        f"{state.get('session_id')}"
    )

    print(
        f"History: "
        f"{len(state.get('conversation_history', []))}"
    )

    print(
        f"Symptoms: "
        f"{state.get('symptoms')}"
    )

    print(
        f"Age: "
        f"{state.get('age')}"
    )

    print(
        f"Duration: "
        f"{state.get('duration')}"
    )

    print(
        f"Severity: "
        f"{state.get('severity')}"
    )

    print(
        f"Missing Information: "
        f"{state.get('missing_information')}"
    )

    print(
        f"Next Question: "
        f"{state.get('next_question')}"
    )

    print(
        f"Risk Level: "
        f"{state.get('risk_level')}"
    )

    print(
        f"Confidence: "
        f"{state.get('confidence')}"
    )

    print(
        f"Supervisor: "
        f"{state.get('supervisor_status')}"
    )

    print(
        f"Result ID: "
        f"{state.get('result_id')}"
    )

    print("========================================\n")

    # =========================================================
    # Assertions
    # =========================================================

    # Session must be created.
    assert state.get("session_id") is not None

    # Conversation history must contain the interaction.
    assert len(
        state.get("conversation_history", [])
    ) >= 1

    # Both symptoms must be extracted.
    symptoms = state.get("symptoms", [])

    assert "chest pain" in symptoms
    assert "shortness of breath" in symptoms

    # =========================================================
    # Critical Assertion
    # =========================================================
    #
    # Because chest pain + shortness of breath is handled
    # as an immediate high-risk scenario, the planner should
    # not stop the pipeline waiting for age/duration/severity.
    #
    # =========================================================

    assert state.get("risk_level") is not None

    # Risk should be HIGH for this scenario.
    assert state.get("risk_level") == "HIGH"

    # Risk assessment must produce confidence.
    assert state.get("confidence") is not None

    # Supervisor must process the result.
    assert state.get("supervisor_status") is not None

    # Persistence must create a database result.
    assert state.get("result_id") is not None

    print("High-risk triage test PASSED.")


if __name__ == "__main__":
    test_high_risk_triage()