from langgraph.graph import StateGraph, END

from state.triage_state import TriageState

from agents.session_agent import session_agent
from agents.conversation_agent import conversation_agent
from agents.general_conversation_agent import (
    general_conversation_agent,
)

from agents.symptom_agent import symptom_agent
from agents.planner_agent import planner_agent
from agents.risk_agent import risk_agent
from agents.supervisor_agent import supervisor_agent
from agents.persistence_agent import persistence_agent

from application.config.llm_config import LLMConfig
from infrastructure.llm.llm_factory import create_llm


# =============================================================
# Intent Router
# =============================================================

def route_intent(state):

    intent = str(
        state.get("intent") or ""
    ).upper()

    # ---------------------------------------------------------
    # Active triage context has priority over GENERAL
    # ---------------------------------------------------------

    if (
        state.get("symptoms")
        or state.get("missing_information")
        or state.get("next_question") is not None
    ):
        return "triage"

    # ---------------------------------------------------------
    # Explicit TRIAGE
    # ---------------------------------------------------------

    if intent == "TRIAGE":
        return "triage"

    # ---------------------------------------------------------
    # Explicit GENERAL
    # ---------------------------------------------------------

    if intent == "GENERAL":
        return "general"

    # ---------------------------------------------------------
    # Default
    # ---------------------------------------------------------

    return "general"


# =============================================================
# Planner Router
# =============================================================

def route_planner(state):

    if state.get(
        "immediate_high_risk",
        False,
    ):
        return "risk"

    missing_information = (
        state.get("missing_information")
        or []
    )

    if missing_information:
        return "ask"

    return "risk"


# =============================================================
# General Conversation Wrapper
# =============================================================

def general_conversation(
    state,
    llm_service=None,
):

    return general_conversation_agent(
        state,
        llm_service=llm_service,
    )


# =============================================================
# Debug Node
# =============================================================

def debug_risk_state(state):

    print(
        "\n========== RISK DEBUG =========="
    )

    print(
        "Risk:",
        state.get("risk_level"),
    )

    print(
        "Confidence:",
        state.get("confidence"),
    )

    print(
        "Recommendation:",
        state.get("recommendation"),
    )

    print(
        "================================\n"
    )

    return state


# =============================================================
# Build Graph
# =============================================================

def build_triage_graph(
    llm_service=None,
):

    graph = StateGraph(
        TriageState
    )

    # =========================================================
    # Session
    #
    # Session must be created before intent routing.
    # GENERAL conversations also belong to a conversation
    # session and therefore require a session_id.
    # =========================================================

    graph.add_node(
        "session",
        session_agent,
    )

    # =========================================================
    # Conversation
    # =========================================================

    graph.add_node(
        "conversation",
        lambda state:
            conversation_agent(
                state,
                llm_service=llm_service,
            ),
    )

    # =========================================================
    # General Conversation
    # =========================================================

    graph.add_node(
        "general_conversation",
        lambda state:
            general_conversation(
                state,
                llm_service=llm_service,
            ),
    )

    # =========================================================
    # Triage
    # =========================================================

    graph.add_node(
        "symptom_analysis",
        symptom_agent,
    )

    graph.add_node(
        "planner",
        planner_agent,
    )

    graph.add_node(
        "risk_assessment",
        lambda state:
            risk_agent(
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

    graph.set_entry_point(
        "session"
    )

    # =========================================================
    # Session -> Conversation
    # =========================================================

    graph.add_edge(
        "session",
        "conversation",
    )

    # =========================================================
    # Intent Routing
    # =========================================================

    graph.add_conditional_edges(
        "conversation",
        route_intent,
        {
            "triage": "symptom_analysis",
            "general": "general_conversation",
        },
    )

    # =========================================================
    # GENERAL FLOW
    # =========================================================

    graph.add_edge(
        "general_conversation",
        END,
    )

    # =========================================================
    # TRIAGE FLOW
    # =========================================================

    graph.add_edge(
        "symptom_analysis",
        "planner",
    )

    graph.add_conditional_edges(
        "planner",
        route_planner,
        {
            "ask": END,
            "risk": "risk_assessment",
        },
    )

    graph.add_edge(
        "risk_assessment",
        "debug_risk",
    )

    graph.add_edge(
        "debug_risk",
        "supervisor",
    )

    graph.add_edge(
        "supervisor",
        "persistence",
    )

    graph.add_edge(
        "persistence",
        END,
    )

    return graph.compile()


# =============================================================
# LLM Configuration
# =============================================================

llm_config = LLMConfig(
    provider="ollama",
    model="gemma3",
)


llm_service = create_llm(
    llm_config
)


# =============================================================
# Global Graph
# =============================================================

triage_graph = build_triage_graph(
    llm_service=llm_service
)