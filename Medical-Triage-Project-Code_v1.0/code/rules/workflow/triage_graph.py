```python
from langgraph.graph import StateGraph, END

from state.triage_state import TriageState

from agents.session_agent import session_agent
from agents.symptom_agent import symptom_agent
from agents.planner_agent import planner_agent
from agents.risk_agent import risk_agent
from agents.supervisor_agent import supervisor_agent
from agents.persistence_agent import persistence_agent


def check_information(state):
    """
    Decide whether enough information exists
    to continue to risk assessment.
    """

    if state.get("missing_information"):
        return "incomplete"

    return "complete"


def build_triage_graph(llm_service=None):
    """
    Build and compile the medical triage graph.

    llm_service is injected into agents that require LLM capabilities.
    """

    graph = StateGraph(TriageState)

    # -------------------------
    # Nodes
    # -------------------------

    graph.add_node(
        "session",
        session_agent,
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
        "supervisor",
        supervisor_agent,
    )

    graph.add_node(
        "persistence",
        persistence_agent,
    )

    # -------------------------
    # Entry point
    # -------------------------

    graph.set_entry_point("session")

    # -------------------------
    # Session → Symptom
    # -------------------------

    graph.add_edge(
        "session",
        "symptom_analysis",
    )

    # -------------------------
    # Symptom → Planner
    # -------------------------

    graph.add_edge(
        "symptom_analysis",
        "planner",
    )

    # -------------------------
    # Planner decision
    # -------------------------

    graph.add_conditional_edges(
        "planner",
        check_information,
        {
            "incomplete": END,
            "complete": "risk_assessment",
        },
    )

    # -------------------------
    # Risk → Supervisor
    # -------------------------

    graph.add_edge(
        "risk_assessment",
        "supervisor",
    )

    # -------------------------
    # Supervisor → Persistence
    # -------------------------

    graph.add_edge(
        "supervisor",
        "persistence",
    )

    # -------------------------
    # Persistence → END
    # -------------------------

    graph.add_edge(
        "persistence",
        END,
    )

    return graph.compile()


# Default graph without LLM.
#
# This preserves the existing import:
#
#     from workflow.triage_graph import triage_graph
#
triage_graph = build_triage_graph()
```
