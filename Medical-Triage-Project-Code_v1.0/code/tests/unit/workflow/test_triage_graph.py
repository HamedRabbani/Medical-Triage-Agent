from workflow.triage_graph import build_triage_graph


def test_build_triage_graph_without_llm():

    graph = build_triage_graph()

    assert graph is not None