from langgraph.graph import StateGraph, END

from state.triage_state import TriageState

from agents.symptom_agent import symptom_agent
from agents.planner_agent import planner_agent
from agents.risk_agent import risk_agent
from agents.supervisor_agent import supervisor_agent


def check_information(state):

    if state.get("missing_information"):
        return "incomplete"

    return "complete"


graph = StateGraph(TriageState)

graph.add_node(
    "symptom_analysis",
    symptom_agent
)

graph.add_node(
    "planner",
    planner_agent
)

graph.add_node(
    "risk_assessment",
    risk_agent
)

graph.add_node(
    "supervisor",
    supervisor_agent
)

graph.set_entry_point(
    "symptom_analysis"
)

graph.add_edge(
    "symptom_analysis",
    "planner"
)

graph.add_conditional_edges(
    "planner",
    check_information,
    {
        "incomplete": END,
        "complete": "risk_assessment",
    },
)

graph.add_edge(
    "risk_assessment",
    "supervisor"
)

graph.add_edge(
    "supervisor",
    END
)

triage_graph = graph.compile()