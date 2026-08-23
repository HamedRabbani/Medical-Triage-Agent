from langgraph.graph import END, StateGraph

from state.triage_state import TriageState

from agents.profile_agent import profile_agent
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

from application.config.settings import Settings
from application.config.llm_provider import build_llm
from application.services.patient_service import PatientService

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

    Priority:
    1. PROFILE
    2. Active TRIAGE
    3. TRIAGE
    4. GENERAL
    """

    intent = str(
        state.get("intent") or ""
    ).upper()

    # ---------------------------------------------------------
    # PROFILE
    # ---------------------------------------------------------

    if intent == "PROFILE":
        return "profile"

    # ---------------------------------------------------------
    # Active TRIAGE
    # ---------------------------------------------------------

    if _is_active_triage(state):
        return "triage"

    # ---------------------------------------------------------
    # Normal intent
    # ---------------------------------------------------------

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
# General Conversation
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
# Profile
# =============================================================

def profile(
    state,
    patient_service=None,
):
    return profile_agent(
        state,
        patient_service=patient_service,
    )


# =============================================================
# Debug
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
    patient_service=None,
):
    """
    Build and compile the medical triage graph.

    Dependencies are injectable so tests can provide
    mocks/fakes without creating real infrastructure.

    If infrastructure dependencies are omitted, they are
    created automatically for backward compatibility.
    """

    # ---------------------------------------------------------
    # Default infrastructure
    # ---------------------------------------------------------

    if database_backend is None:

        settings = Settings()

        database_backend = (
            create_database_backend(
                settings
            )
        )

    # ---------------------------------------------------------
    # Patient service
    # ---------------------------------------------------------

    if patient_service is None:

        patient_service = PatientService(
            database_backend.patient
        )

    # ---------------------------------------------------------
    # LLM
    # ---------------------------------------------------------

    if llm_service is None:

        settings = Settings()

        llm_service = build_llm(
            settings
        )

    # ---------------------------------------------------------
    # Graph
    # ---------------------------------------------------------

    graph = StateGraph(
        TriageState
    )

    # =========================================================
    # Session
    # =========================================================

    graph.add_node(
        "session",
        lambda state:
            session_agent(
                state,
                database_backend=database_backend,
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
    # Profile
    # =========================================================

    graph.add_node(
        "profile",
        lambda state:
            profile(
                state,
                patient_service=patient_service,
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
    # Symptom Analysis
    # =========================================================

    graph.add_node(
        "symptom_analysis",
        symptom_agent,
    )

    # =========================================================
    # Planner
    # =========================================================

    graph.add_node(
        "planner",
        planner_agent,
    )

    # =========================================================
    # Risk Assessment
    # =========================================================

    graph.add_node(
        "risk_assessment",
        lambda state:
            risk_agent(
                state,
                llm_service=llm_service,
            ),
    )

    # =========================================================
    # Debug Risk
    # =========================================================

    graph.add_node(
        "debug_risk",
        debug_risk_state,
    )

    # =========================================================
    # Supervisor
    # =========================================================

    graph.add_node(
        "supervisor",
        supervisor_agent,
    )

    # =========================================================
    # Persistence
    # =========================================================

    graph.add_node(
        "persistence",
        lambda state:
            persistence_agent(
                state,
                database_backend=database_backend,
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
            "profile": "profile",
            "triage": "symptom_analysis",
            "general": "general_conversation",
        },
    )

    # =========================================================
    # PROFILE FLOW
    # =========================================================

    graph.add_edge(
        "profile",
        END,
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
# Global Graph
#
# Legacy / direct-import compatibility
# =============================================================

settings = Settings()

llm_service = build_llm(
    settings
)

database_backend = create_database_backend(
    settings
)

patient_service = PatientService(
    database_backend.patient
)

triage_graph = build_triage_graph(
    llm_service=llm_service,
    database_backend=database_backend,
    patient_service=patient_service,
)