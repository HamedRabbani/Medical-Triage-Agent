from langgraph.graph import END, StateGraph

from state.triage_state import TriageState

from agents.profile_agent import profile_agent
from agents.session_agent import session_agent
from agents.conversation_agent import conversation_agent
from agents.general_conversation_agent import (
    general_conversation_agent,
)
from agents.rag_agent import rag_agent
from agents.symptom_agent import symptom_agent
from agents.planner_agent import planner_agent
from agents.risk_agent import risk_agent
from agents.supervisor_agent import supervisor_agent
from agents.persistence_agent import persistence_agent
from agents.medical_response_agent import (
    medical_response_agent,
)

from application.config.settings import Settings
from application.config.llm_provider import build_llm
from application.services.patient_service import PatientService
from application.services.conversation_service import (
    ConversationService,
)
from application.services.triage_service import (
    TriageService,
)
from application.services.triage_agent_service import (
    TriageAgentService,
)

from infrastructure.database.conversation_persistence_factory import (
    create_database_backend,
)

from infrastructure.rag.rag_factory import (
    create_rag_service,
)


# =============================================================
# Intent Routing
# =============================================================

def _is_active_triage(state) -> bool:

    if state.get("missing_information"):
        return True

    if state.get("next_question") is not None:
        return True

    return False


def route_intent(state):

    intent = str(
        state.get("intent") or ""
    ).upper()

    if intent == "PROFILE":
        return "profile"

    if _is_active_triage(state):
        return "triage"

    if intent == "TRIAGE":
        return "triage"

    if intent == "GENERAL":
        return "general"

    return "general"


# =============================================================
# Planner Routing
# =============================================================

def route_planner(state):

    # Immediate high-risk cases must not wait
    # for additional information.
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
# Supervisor Routing
# =============================================================

def route_supervisor(state):

    status = state.get(
        "supervisor_status"
    )

    # Approved assessment can proceed
    # to patient-facing response.
    if status == "APPROVED":
        return "response"

    # Conflicting rule/LLM assessment requires
    # review, but the patient should still receive
    # a safe response based on the deterministic
    # triage decision.
    if status == "REVIEW_REQUIRED":
        return "response"

    # Rejected assessment must not be presented
    # as a valid patient-facing assessment.
    if status == "REJECTED":
        return "end"

    return "end"


# =============================================================
# Agent Wrappers
# =============================================================

def general_conversation(
    state,
    llm_service=None,
    database_backend=None,
):
    """
    Generate GENERAL response and persist the
    assistant message.

    The actual response generation remains inside
    general_conversation_agent.

    Persistence is handled here because the current
    DatabaseBackend exposes message creation through
    the triage persistence port.
    """

    # ---------------------------------------------------------
    # Generate assistant response
    # ---------------------------------------------------------

    state = general_conversation_agent(
        state,
        llm_service=llm_service,
    )

    response = state.get(
        "assistant_response"
    )

    session_id = state.get(
        "session_id"
    )

    # ---------------------------------------------------------
    # Safety checks
    # ---------------------------------------------------------

    if not response:
        return state

    if session_id is None:
        return state

    if database_backend is None:
        return state

    # ---------------------------------------------------------
    # Persist assistant message
    # ---------------------------------------------------------

    triage_service = TriageService(
        database_backend.triage
    )

    agent_service = TriageAgentService(
        triage_service
    )

    agent_service.add_message(
        session_id=session_id,
        content=response,
        sender_type="Agent",
    )

    database_backend.triage.commit()

    # ---------------------------------------------------------
    # Reload conversation history
    # ---------------------------------------------------------

    conversation_service = ConversationService(
        database_backend.conversation
    )

    history = conversation_service.get_history(
        session_id
    )

    # ---------------------------------------------------------
    # Return updated state
    # ---------------------------------------------------------

    return {
        **state,
        "conversation_history": history,
        "assistant_response": response,
        "response": response,
    }


def profile(
    state,
    patient_service=None,
):
    return profile_agent(
        state,
        patient_service=patient_service,
    )


def retrieve_medical_knowledge(
    state,
    rag_service=None,
):
    return rag_agent(
        state,
        rag_service=rag_service,
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
        "LLM Risk:",
        state.get("llm_risk_level"),
    )

    print(
        "LLM Confidence:",
        state.get("llm_confidence"),
    )

    print(
        "Supervisor:",
        state.get("supervisor_status"),
    )

    print(
        "================================\n"
    )

    return state


def debug_supervisor_state(state):

    print(
        "\n========== SUPERVISOR DEBUG =========="
    )

    print(
        "Rule Risk:",
        state.get("risk_level"),
    )

    print(
        "LLM Risk:",
        state.get("llm_risk_level"),
    )

    print(
        "Supervisor Status:",
        state.get("supervisor_status"),
    )

    print(
        "======================================\n"
    )

    return state


# =============================================================
# Graph Builder
# =============================================================

def build_triage_graph(
    llm_service=None,
    database_backend=None,
    patient_service=None,
    rag_service=None,
):

    # ---------------------------------------------------------
    # Dependencies
    # ---------------------------------------------------------

    if database_backend is None:

        settings = Settings()

        database_backend = (
            create_database_backend(
                settings
            )
        )

    if patient_service is None:

        patient_service = PatientService(
            database_backend.patient
        )

    if llm_service is None:

        settings = Settings()

        llm_service = build_llm(
            settings
        )

    if rag_service is None:

        rag_service = create_rag_service()

    # ---------------------------------------------------------
    # State Graph
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
    # Conversation / Intent
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
                database_backend=database_backend,
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
    # RAG
    # =========================================================

    graph.add_node(
        "rag_retrieval",
        lambda state:
            retrieve_medical_knowledge(
                state,
                rag_service=rag_service,
            ),
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

    graph.add_node(
        "debug_supervisor",
        debug_supervisor_state,
    )

    # =========================================================
    # Medical Response
    # =========================================================

    graph.add_node(
        "medical_response",
        lambda state:
            medical_response_agent(
                state,
                llm_service=llm_service,
            ),
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
    # Entry Point
    # =========================================================

    graph.set_entry_point(
        "session"
    )

    # =========================================================
    # Session → Conversation
    # =========================================================

    graph.add_edge(
        "session",
        "conversation",
    )

    # =========================================================
    # Conversation → Intent
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
    # Profile → END
    # =========================================================

    graph.add_edge(
        "profile",
        END,
    )

    # =========================================================
    # General Conversation → END
    # =========================================================

    graph.add_edge(
        "general_conversation",
        END,
    )

    # =========================================================
    # Symptom Analysis → Planner
    # =========================================================

    graph.add_edge(
        "symptom_analysis",
        "planner",
    )

    # =========================================================
    # Planner Routing
    # =========================================================

    graph.add_conditional_edges(
        "planner",
        route_planner,
        {
            # More information is required.
            # End this turn and wait for the
            # next user message.
            "ask": END,

            # Enough information or immediate
            # high-risk condition.
            "risk": "rag_retrieval",
        },
    )

    # =========================================================
    # RAG → Risk
    # =========================================================

    graph.add_edge(
        "rag_retrieval",
        "risk_assessment",
    )

    # =========================================================
    # Risk → Debug
    # =========================================================

    graph.add_edge(
        "risk_assessment",
        "debug_risk",
    )

    # =========================================================
    # Debug Risk → Supervisor
    # =========================================================

    graph.add_edge(
        "debug_risk",
        "supervisor",
    )

    # =========================================================
    # Supervisor → Debug
    # =========================================================

    graph.add_edge(
        "supervisor",
        "debug_supervisor",
    )

    # =========================================================
    # Supervisor Gate
    # =========================================================

    graph.add_conditional_edges(
        "debug_supervisor",
        route_supervisor,
        {
            "response": "medical_response",
            "end": END,
        },
    )

    # =========================================================
    # Medical Response → Persistence
    # =========================================================

    graph.add_edge(
        "medical_response",
        "persistence",
    )

    # =========================================================
    # Persistence → END
    # =========================================================

    graph.add_edge(
        "persistence",
        END,
    )

    # =========================================================
    # Compile
    # =========================================================

    return graph.compile()


# =============================================================
# Application-level Dependencies
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

rag_service = create_rag_service()


# =============================================================
# Application-level Graph
# =============================================================

triage_graph = build_triage_graph(
    llm_service=llm_service,
    database_backend=database_backend,
    patient_service=patient_service,
    rag_service=rag_service,
)