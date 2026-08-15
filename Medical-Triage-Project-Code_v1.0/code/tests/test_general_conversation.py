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


def test_general_conversation() -> None:
    """
    Test a real GENERAL conversation.

    Scenario:
        User sends a general non-medical message.

    Expected behavior:
        - Session is created.
        - Message is stored in conversation history.
        - Intent is GENERAL.
        - No medical symptoms are extracted.
        - No risk assessment is performed.
        - No TriageResult is created.
        - A general assistant response is returned.
    """

    # =========================================================
    # Initial State
    # =========================================================

    state = {
        "patient_id": 2,
        "session_id": None,

        "user_message": "",

        "intent": None,

        "age": None,
        "symptoms": [],
        "severity": None,
        "duration": None,

        "red_flags": [],
        "missing_information": [],
        "next_question": None,

        "risk_level": None,
        "confidence": None,

        "supervisor_status": None,
        "recommendation": None,

        "conversation_history": [],
        "result_id": None,

        "assistant_response": None,
        "response": None,
    }

    # =========================================================
    # Turn 1
    # =========================================================

    state = invoke_turn(
        state,
        "Hello, how are you?",
    )

    print("\n========================================")
    print("GENERAL CONVERSATION TEST")
    print("========================================")

    print(f"Session ID: {state.get('session_id')}")
    print(f"History: {len(state.get('conversation_history', []))}")
    print(f"Intent: {state.get('intent')}")
    print(f"Symptoms: {state.get('symptoms')}")
    print(f"Risk Level: {state.get('risk_level')}")
    print(f"Supervisor: {state.get('supervisor_status')}")
    print(f"Result ID: {state.get('result_id')}")
    print(f"Response: {state.get('assistant_response')}")

    print("========================================")

    # =========================================================
    # Session
    # =========================================================

    assert state.get("session_id") is not None

    # =========================================================
    # Conversation History
    # =========================================================

    assert len(
        state.get("conversation_history", [])
    ) >= 2

    # =========================================================
    # Intent
    # =========================================================

    assert state.get("intent") == "GENERAL"

    # =========================================================
    # No Triage Processing
    # =========================================================

    assert state.get("symptoms") == []

    assert state.get("risk_level") is None

    assert state.get("confidence") is None

    assert state.get("supervisor_status") is None

    assert state.get("result_id") is None

    # =========================================================
    # General Response
    # =========================================================

    response = state.get("assistant_response")

    assert response is not None
    assert isinstance(response, str)
    assert response.strip() != ""

    print("\nGeneral conversation test PASSED.")


if __name__ == "__main__":
    test_general_conversation()