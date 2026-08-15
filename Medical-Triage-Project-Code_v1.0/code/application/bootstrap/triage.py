from application.config.llm_settings import load_llm_config
from application.services.llm_service import LLMService
from infrastructure.llm.llm_factory import create_llm

from workflow.triage_graph import build_triage_graph


def create_triage_graph():
    config = load_llm_config()

    llm_adapter = create_llm(config)

    llm_service = LLMService(
        llm_adapter
    )

    return build_triage_graph(
        llm_service=llm_service
    )