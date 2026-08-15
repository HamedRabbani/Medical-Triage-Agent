from application.config.llm_provider import build_llm
from application.config.settings import Settings
from application.services.llm_service import LLMService

from workflow.triage_graph import build_triage_graph


def main():

    # Build real LLM
    llm = build_llm(Settings())
    llm_service = LLMService(llm)

    # Build graph with LLM dependency
    graph = build_triage_graph(
        llm_service=llm_service,
    )

    state = {
        "patient_id": 2,
        "user_message": "من تب و سردرد دارم",
        "conversation_history": [],
        "symptoms": [],
        "age": None,
        "duration": None,
        "severity": None,
        "missing_information": False,
    }

    result = graph.invoke(state)

    print("\nFINAL STATE:")
    print(result)

    print("\nSYMPTOMS:")
    print(result.get("symptoms"))


if __name__ == "__main__":
    main()