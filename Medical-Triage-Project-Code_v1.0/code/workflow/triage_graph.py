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

    """
    Decide conversation flow.

    GENERAL:
        Normal conversation
        Admin/Doctor without patient context

    TRIAGE:
        Patient medical assessment
    """


    intent = state.get(
        "intent"
    )


    roles = [
        str(role).lower()
        for role in state.get(
            "user_roles",
            []
        )
    ]


    patient_id = state.get(
        "patient_id"
    )


    # ---------------------------------------------------------
    # Explicit TRIAGE request
    # ---------------------------------------------------------

    if intent == "TRIAGE":


        # Admin / Doctor without selected patient
        if (
            "patient" not in roles
            and patient_id is None
        ):

            return "general"


        return "triage"



    # ---------------------------------------------------------
    # Explicit GENERAL request
    # ---------------------------------------------------------

    if intent == "GENERAL":

        return "general"



    # ---------------------------------------------------------
    # Existing symptom context
    # ---------------------------------------------------------

    if state.get(
        "symptoms"
    ):


        if (
            "patient" in roles
            and patient_id is not None
        ):

            return "triage"


        return "general"



    # ---------------------------------------------------------
    # Default
    # ---------------------------------------------------------

    return "general"





# =============================================================
# Planner Router
# =============================================================

def route_planner(state):

    missing_information = (
        state.get(
            "missing_information"
        )
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
        state.get(
            "risk_level"
        )
    )


    print(
        "Confidence:",
        state.get(
            "confidence"
        )
    )


    print(
        "Recommendation:",
        state.get(
            "recommendation"
        )
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
    # Nodes
    # =========================================================


    graph.add_node(
        "conversation",
        lambda state:
            conversation_agent(
                state,
                llm_service=llm_service,
            ),
    )



    graph.add_node(
        "general_conversation",
        lambda state:
            general_conversation(
                state,
                llm_service=llm_service,
            ),
    )



    # -------------------------
    # Triage only
    # -------------------------

    graph.add_node(
        "session",
        session_agent,
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
        "conversation"
    )



    # =========================================================
    # Intent Routing
    # =========================================================


    graph.add_conditional_edges(
        "conversation",

        route_intent,

        {
            "triage":
                "session",

            "general":
                "general_conversation",
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
        "session",
        "symptom_analysis",
    )


    graph.add_edge(
        "symptom_analysis",
        "planner",
    )



    graph.add_conditional_edges(
        "planner",

        route_planner,

        {
            "ask":
                END,

            "risk":
                "risk_assessment",
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