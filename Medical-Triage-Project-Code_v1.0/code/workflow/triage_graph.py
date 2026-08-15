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
# Intent Router
# =============================================================

def route_intent(state):
    """
    Route the conversation according to intent.

    TRIAGE  -> medical triage pipeline
    GENERAL -> general conversation

    Backward compatibility is preserved for older tests
    that directly provide clinical information.
    """

    intent = state.get("intent")

    if intent == "TRIAGE":
        return "triage"

    if intent == "GENERAL":
        return "general"

    # Legacy/direct triage flow
    if (
        state.get("symptoms")
        or state.get("severity") is not None
        or state.get("duration") is not None
        or state.get("age") is not None
    ):
        return "triage"

    # Existing full-triage tests may provide only user_message.
    # Let Conversation Agent handle those messages.
    user_message = state.get(
        "user_message",
        "",
    )

    if isinstance(user_message, str):
        medical_terms = {
            "pain",
            "chest",
            "fever",
            "cough",
            "headache",
            "shortness",
            "breath",
            "bleeding",
            "vomiting",
            "dizziness",
        }

        words = set(
            user_message.lower().split()
        )

        if words.intersection(medical_terms):
            return "triage"

    return "general"


# =============================================================
# Planner Router
# =============================================================

def check_information(state):
    """
    Decide whether enough clinical information exists
    for risk assessment.

    Age is NOT mandatory for initial risk assessment.
    """

    symptoms = state.get("symptoms") or []
    severity = state.get("severity")
    duration = state.get("duration")

    if (
        symptoms
        and severity is not None
        and duration is not None
    ):
        return "complete"

    return "incomplete"


# =============================================================
# General Conversation
# =============================================================

def general_conversation(state):
    """
    Handle a general conversation.

    Current baseline response is deterministic.
    LLM-based general response generation can be introduced
    later without changing the routing architecture.
    """

    response = "Hello. How can I help you?"

    return {
        **state,
        "assistant_response": response,
        "response": response,
    }


# =============================================================
# Risk Debug Node
# =============================================================

def debug_risk_state(state):
    """
    Temporary debugging node.
    """

    print("\n========== AFTER RISK AGENT ==========")

    print(
        "risk_level:",
        state.get("risk_level"),
    )

    print(
        "confidence:",
        state.get("confidence"),
    )

    print(
        "red_flags:",
        state.get("red_flags"),
    )

    print(
        "recommendation:",
        state.get("recommendation"),
    )

    print("\n--- LLM RESULT ---")

    print(
        "llm_risk_level:",
        state.get("llm_risk_level"),
    )

    print(
        "llm_confidence:",
        state.get("llm_confidence"),
    )

    print(
        "llm_red_flags:",
        state.get("llm_red_flags"),
    )

    print(
        "llm_recommendation:",
        state.get("llm_recommendation"),
    )

    print("=======================================\n")

    return state


# =============================================================
# Build Graph
# =============================================================

def build_triage_graph(llm_service=None):

    graph = StateGraph(TriageState)

    # ---------------------------------------------------------
    # Nodes
    # ---------------------------------------------------------

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
        "general_conversation",
        general_conversation,
    )

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

    # ---------------------------------------------------------
    # Entry
    # ---------------------------------------------------------

    graph.set_entry_point("session")

    # ---------------------------------------------------------
    # Session → Conversation
    # ---------------------------------------------------------

    graph.add_edge(
        "session",
        "conversation",
    )

    # ---------------------------------------------------------
    # Conversation → Intent
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "conversation",
        route_intent,
        {
            "triage": "symptom_analysis",
            "general": "general_conversation",
        },
    )

    # ---------------------------------------------------------
    # General → END
    # ---------------------------------------------------------

    graph.add_edge(
        "general_conversation",
        END,
    )

    # ---------------------------------------------------------
    # Symptom → Planner
    # ---------------------------------------------------------

    graph.add_edge(
        "symptom_analysis",
        "planner",
    )

    # ---------------------------------------------------------
    # Planner → Risk / END
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "planner",
        check_information,
        {
            "incomplete": END,
            "complete": "risk_assessment",
        },
    )

    # ---------------------------------------------------------
    # Risk → Debug
    # ---------------------------------------------------------

    graph.add_edge(
        "risk_assessment",
        "debug_risk",
    )

    # ---------------------------------------------------------
    # Debug → Supervisor
    # ---------------------------------------------------------

    graph.add_edge(
        "debug_risk",
        "supervisor",
    )

    # ---------------------------------------------------------
    # Supervisor → Persistence
    # ---------------------------------------------------------

    graph.add_edge(
        "supervisor",
        "persistence",
    )

    # ---------------------------------------------------------
    # Persistence → END
    # ---------------------------------------------------------

    graph.add_edge(
        "persistence",
        END,
    )

    return graph.compile()


# =============================================================
# Default Graph
# =============================================================

triage_graph = build_triage_graph()