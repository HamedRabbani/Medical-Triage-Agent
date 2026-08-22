from application.config.settings import Settings
from application.config.llm_provider import build_llm

from langgraph.graph import END, StateGraph

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

from infrastructure.database.conversation_persistence_factory import (
    create_database_backend,
)


# =============================================================
# Active Triage Detection
# =============================================================

def _is_active_triage(state) -> bool:
    """
    Determine whether the conversation is already
    inside an active medical triage flow.
    """

    if state.get("missing_information"):
        return True

    if state.get("next_question") is not None:
        return True

    return False


# =============================================================
# Intent Router
# =============================================================

def route_intent(state):
    """
    Route the conversation after intent detection.

    Active triage has priority over GENERAL.
    """

    # ---------------------------------------------------------
    # Active triage always remains TRIAGE
    # ---------------------------------------------------------

    if _is_active_triage(state):
        return "triage"

    # ---------------------------------------------------------
    # Normal intent routing
    # ---------------------------------------------------------

    intent = str(
        state.get("intent") or ""
    ).upper()

    if intent == "TRIAGE":
        return "triage"

    if intent == "GENERAL":
        return "general"

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
    database_backend=None,
):

    graph = StateGraph(
        TriageState
    )

    settings = Settings()

    # ---------------------------------------------------------
    # Database Backend
    # ---------------------------------------------------------

    backend = database_backend

    if backend is None:
        backend = create_database_backend(
            settings
        )

    # =========================================================
    # Session
    # =========================================================

    graph.add_node(
        "session",
        lambda state:
            session_agent(
                state,
                database_backend=backend,
            ),
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
        lambda state:
            persistence_agent(
                state,
                database_backend=backend,
            ),
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

settings = Settings()

llm_service = build_llm(
    settings
)


# =============================================================
# Global Graph
# =============================================================

database_backend = create_database_backend(
    settings
)

triage_graph = build_triage_graph(
    llm_service=llm_service,
    database_backend=database_backend,
)