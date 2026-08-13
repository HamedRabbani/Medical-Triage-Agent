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


def test_full_triage_flow() -> None:
    """Test a real multi-turn triage conversation."""

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

        "supervisor_status": None,
        "recommendation": None,

        "conversation_history": [],
        "result_id": None,
    }

    # ---------------------------------
    # Turn 1
    # ---------------------------------

    state = invoke_turn(
        state,
        "I have chest pain.",
    )

    print("\n=== Turn 1 ===")
    print(f"Session ID: {state.get('session_id')}")
    print(f"History: {len(state.get('conversation_history', []))}")
    print(f"Age: {state.get('age')}")
    print(f"Symptoms: {state.get('symptoms')}")
    print(f"Duration: {state.get('duration')}")
    print(f"Severity: {state.get('severity')}")
    print(f"Question: {state.get('next_question')}")

    assert state.get("session_id") is not None
    assert len(state.get("conversation_history", [])) >= 1
    assert "chest pain" in state.get("symptoms", [])

    session_id = state["session_id"]

    # ---------------------------------
    # Turn 2
    # ---------------------------------

    state = invoke_turn(
        state,
        "29",
    )

    print("\n=== Turn 2 ===")
    print(f"Session ID: {state.get('session_id')}")
    print(f"History: {len(state.get('conversation_history', []))}")
    print(f"Age: {state.get('age')}")
    print(f"Symptoms: {state.get('symptoms')}")
    print(f"Duration: {state.get('duration')}")
    print(f"Severity: {state.get('severity')}")
    print(f"Question: {state.get('next_question')}")

    assert state["session_id"] == session_id
    assert state["age"] == 29

    # ---------------------------------
    # Turn 3
    # ---------------------------------

    state = invoke_turn(
        state,
        "It started 20 minutes ago.",
    )

    print("\n=== Turn 3 ===")
    print(f"Session ID: {state.get('session_id')}")
    print(f"History: {len(state.get('conversation_history', []))}")
    print(f"Age: {state.get('age')}")
    print(f"Symptoms: {state.get('symptoms')}")
    print(f"Duration: {state.get('duration')}")
    print(f"Severity: {state.get('severity')}")
    print(f"Question: {state.get('next_question')}")

    assert state["session_id"] == session_id
    assert state["age"] == 29
    assert state["duration"] == "20 minutes"

    # ---------------------------------
    # Turn 4
    # ---------------------------------

    state = invoke_turn(
        state,
        "زیاد",
    )

    print("\n=== Turn 4 ===")
    print(f"Session ID: {state.get('session_id')}")
    print(f"History: {len(state.get('conversation_history', []))}")
    print(f"Age: {state.get('age')}")
    print(f"Symptoms: {state.get('symptoms')}")
    print(f"Duration: {state.get('duration')}")
    print(f"Severity: {state.get('severity')}")
    print(f"Risk: {state.get('risk_level')}")
    print(f"Confidence: {state.get('confidence')}")
    print(f"Supervisor: {state.get('supervisor_status')}")
    print(f"Result ID: {state.get('result_id')}")

    assert state["session_id"] == session_id
    assert state["age"] == 29
    assert "chest pain" in state["symptoms"]
    assert state["duration"] == "20 minutes"
    assert state["severity"] == "severe"

    assert state.get("risk_level") is not None
    assert state.get("confidence") is not None
    assert state.get("supervisor_status") is not None
    assert state.get("result_id") is not None

    assert len(
        state.get("conversation_history", [])
    ) >= 4

    print("\nFull multi-turn triage flow PASSED.")


if __name__ == "__main__":
    test_full_triage_flow()