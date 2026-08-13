from agents.symptom_agent import symptom_agent
from agents.planner_agent import planner_agent
from agents.risk_agent import risk_agent


def test_triage_reasoning_flow() -> None:
    """Test history-based extraction through risk assessment."""

    state = {
        "user_message": "زیاد",

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

        "patient_id": 2,
        "session_id": 10,

        "conversation_history": [
            {
                "message_id": 1,
                "sender_type": "Patient",
                "content": "I have chest pain.",
            },
            {
                "message_id": 2,
                "sender_type": "Patient",
                "content": "29",
            },
            {
                "message_id": 3,
                "sender_type": "Patient",
                "content": "It started 20 minutes ago.",
            },
            {
                "message_id": 4,
                "sender_type": "Patient",
                "content": "زیاد",
            },
        ],
    }

    # -------------------------
    # Step 1: Symptom Agent
    # -------------------------

    state = symptom_agent(state)

    print("\n=== After Symptom Agent ===")
    print(f"Age: {state.get('age')}")
    print(f"Symptoms: {state.get('symptoms')}")
    print(f"Duration: {state.get('duration')}")
    print(f"Severity: {state.get('severity')}")

    assert state["age"] == 29
    assert "chest pain" in state["symptoms"]
    assert state["duration"] == "20 minutes"
    assert state["severity"] == "severe"

    # -------------------------
    # Step 2: Planner
    # -------------------------

    state = planner_agent(state)

    print("\n=== After Planner ===")
    print(
        f"Missing: "
        f"{state.get('missing_information')}"
    )
    print(
        f"Question: "
        f"{state.get('next_question')}"
    )

    assert state["missing_information"] == []
    assert state["next_question"] is None

    # -------------------------
    # Step 3: Risk Agent
    # -------------------------

    state = risk_agent(state)

    print("\n=== After Risk Agent ===")
    print(
        f"Risk Level: "
        f"{state.get('risk_level')}"
    )
    print(
        f"Confidence: "
        f"{state.get('confidence')}"
    )
    print(
        f"Red Flags: "
        f"{state.get('red_flags')}"
    )

    assert state.get("risk_level") is not None
    assert state.get("confidence") is not None

    print("\nTriage reasoning flow PASSED.")


if __name__ == "__main__":
    test_triage_reasoning_flow()