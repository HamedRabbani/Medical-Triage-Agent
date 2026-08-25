
from application.services.rag_service import (
    RAGService,
)


def rag_agent(
    state,
    rag_service: RAGService,
):
    """
    Retrieval-only RAG agent.

    RAG does not perform risk assessment.
    RAG does not override rule-based triage.
    """

    query_parts: list[str] = []

    symptoms = (
        state.get("symptoms")
        or []
    )

    if symptoms:
        query_parts.append(
            "Symptoms: "
            + ", ".join(symptoms)
        )

    age = state.get("age")

    if age is not None:
        query_parts.append(
            f"Age: {age}"
        )

    duration = state.get(
        "duration"
    )

    if duration:
        query_parts.append(
            f"Duration: {duration}"
        )

    severity = state.get(
        "severity"
    )

    if severity:
        query_parts.append(
            f"Severity: {severity}"
        )

    red_flags = (
        state.get("red_flags")
        or []
    )

    if red_flags:
        query_parts.append(
            "Red flags: "
            + ", ".join(red_flags)
        )

    query = "\n".join(
        query_parts
    )

    if not query.strip():
        return {
            **state,
            "rag_context": [],
        }

    results = rag_service.retrieve(
        query=query,
        top_k=3,
        distance_threshold=20,
    )

    return {
        **state,
        "rag_context": results,
    }
