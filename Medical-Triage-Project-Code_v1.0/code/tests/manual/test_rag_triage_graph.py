from workflow.triage_graph import (
    triage_graph,
    database_backend,
)


def main():
    patient = database_backend.patient.get_patient_by_id(6)

    if patient is None:
        raise RuntimeError(
            "Patient ID 5 does not exist in the configured database."
        )

    state = {
        "patient_id": patient.patient_id,
        "session_id": None,
        "user_message": "من سردرد شدید دارم",

        "age": None,
        "symptoms": [],
        "severity": None,
        "duration": None,

        "red_flags": [],
        "missing_information": [],
        "next_question": None,

        "intent": None,
        "intent_confidence": None,
        "triage_active": False,

        "conversation_history": [],

        "assistant_response": None,
        "response": None,
    }

    result = triage_graph.invoke(state)

    print("\n" + "=" * 60)
    print("RAG TRIAGE GRAPH TEST")
    print("=" * 60)

    print("\nIntent:")
    print(result.get("intent"))

    print("\nSymptoms:")
    print(result.get("symptoms"))

    print("\nRAG Context:")
    for item in result.get("rag_context", []):
        print("-" * 40)
        print("Source:", item.get("source"))
        print("Content:", item.get("content"))
        print("Distance:", item.get("distance"))

    print("\nRule Risk:")
    print(result.get("risk_level"))

    print("\nLLM Risk:")
    print(result.get("llm_risk_level"))

    print("\nRecommendation:")
    print(result.get("recommendation"))

    print("\nAssistant Response:")
    print(result.get("assistant_response"))

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()