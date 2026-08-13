from agents.symptom_agent import symptom_agent


def test_symptom_agent() -> None:
    """Test symptom extraction from conversation history."""

    state = {
        "user_message": "زیاد",
        "age": None,
        "symptoms": [],
        "duration": None,
        "severity": None,
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

    result = symptom_agent(state)

    print("\n=== Symptom Agent Test ===")
    print(f"Age: {result.get('age')}")
    print(f"Symptoms: {result.get('symptoms')}")
    print(f"Duration: {result.get('duration')}")
    print(f"Severity: {result.get('severity')}")

    assert result["age"] == 29
    assert result["duration"] == "20 minutes"
    assert result["severity"] == "severe"
    assert "chest pain" in result["symptoms"]

    print("Symptom agent test PASSED.")


if __name__ == "__main__":
    test_symptom_agent()