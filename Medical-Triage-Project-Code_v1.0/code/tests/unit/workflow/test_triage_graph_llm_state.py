from langgraph.graph import StateGraph, END

from state.triage_state import TriageState

from agents.session_agent import session_agent
from agents.conversation_agent import conversation_agent
from agents.symptom_agent import symptom_agent
from agents.planner_agent import planner_agent
from agents.risk_agent import risk_agent
from agents.supervisor_agent import supervisor_agent
from agents.persistence_agent import persistence_agent


# =============================================================
# Routing
# =============================================================

def route_after_conversation(state: TriageState) -> str:
    """
    Route the conversation according to detected intent.

    TRIAGE  -> continue to symptom analysis
    GENERAL -> end the triage workflow
    """

    intent = state.get("intent")

    if intent == "TRIAGE":
        return "triage"

    return "general"


def check_information(state: TriageState) -> str:
    """
    Decide whether enough information is available
    for risk assessment.
    """

    if state.get("missing_information"):
        return "incomplete"

    return "complete"


# =============================================================
# Debug
# =============================================================

def debug_risk_state(state: TriageState) -> TriageState:
    """
    Temporary debugging node for LLM/rule risk state.
    """

    print("\n========== AFTER RISK AGENT ==========")

    print("risk_level:", state.get("risk_level"))
    print("confidence:", state.get("confidence"))
    print("red_flags:", state.get("red_flags"))
    print("recommendation:", state.get("recommendation"))

    print("\n--- LLM RESULT ---")

    print("llm_risk_level:", state.get("llm_risk_level"))
    print("llm_confidence:", state.get("llm_confidence"))
    print("llm_red_flags:", state.get("llm_red_flags"))
    print("llm_recommendation:", state.get("llm_recommendation"))

    print("=======================================\n")

    return state


# =============================================================
# Graph Builder
# =============================================================

def build_triage_graph(llm_service=None):
    """
    Build the Medical Triage LangGraph.

    LLM is injected through llm_service so that:

    - Unit tests can use mocks.
    - Integration tests can use Ollama/Gemini.
    - The workflow remains provider-agnostic.
    """

    graph = StateGraph(TriageState)

    # =========================================================
    # Nodes
    # =========================================================

    graph.add_node(
        "session",
        session_agent,
    )

    graph.add_node(
        "conversation",
        lambda state: conversation_agent(
            state,
            llm_service=llm_service,
        ),
    )

    graph.add_node(
        "symptom_analysis",
        lambda state: symptom_agent(
            state,
            llm_service=llm_service,
        ),
    )

    graph.add_node(
        "planner",
        planner_agent,
    )

    graph.add_node(
        "risk_assessment",
        lambda state: risk_agent(
            state,
            llm_service=llm_service,
        ),
    )

    graph.add_node(
        "debug_risk",
        debug_risk_state,
    )

    graph.add_node(
        "supervisor",
        supervisor_agent,
    )

    graph.add_node(
        "persistence",
        persistence_agent,
    )

    # =========================================================
    # Entry
    # =========================================================

    graph.set_entry_point("session")

    # =========================================================
    # Session
    # =========================================================

    graph.add_edge(
        "session",
        "conversation",
    )

    # =========================================================
    # Conversation Intent
    # =========================================================

    graph.add_conditional_edges(
        "conversation",
        route_after_conversation,
        {
            "triage": "symptom_analysis",
            "general": END,
        },
    )

    # =========================================================
    # Symptom Analysis
    # =========================================================

    graph.add_edge(
        "symptom_analysis",
        "planner",
    )

    # =========================================================
    # Planner
    # =========================================================

    graph.add_conditional_edges(
        "planner",
        check_information,
        {
            "incomplete": END,
            "complete": "risk_assessment",
        },
    )

    # =========================================================
    # Risk Assessment
    # =========================================================

    graph.add_edge(
        "risk_assessment",
        "debug_risk",
    )

    # =========================================================
    # Supervisor
    # =========================================================

    graph.add_edge(
        "debug_risk",
        "supervisor",
    )

    # =========================================================
    # Persistence
    # =========================================================

    graph.add_edge(
        "supervisor",
        "persistence",
    )

    graph.add_edge(
        "persistence",
        END,
    )

    # =========================================================
    # Compile
    # =========================================================

    return graph.compile()


# =============================================================
# Default Graph
# =============================================================

triage_graph = build_triage_graph()