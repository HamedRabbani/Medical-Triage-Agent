from application.config.settings import Settings
from application.config.llm_settings import load_llm_config

from application.services.llm_service import (
    LLMService,
)

from application.services.patient_service import (
    PatientService,
)

from infrastructure.llm.llm_factory import (
    create_llm,
)

from infrastructure.database.conversation_persistence_factory import (
    create_database_backend,
)

from workflow.triage_graph import (
    build_triage_graph,
)


def create_triage_graph():

    # =========================================================
    # Application Settings
    # =========================================================

    settings = Settings()

    # =========================================================
    # LLM
    # =========================================================

    llm_config = load_llm_config()

    llm_adapter = create_llm(
        llm_config
    )

    llm_service = LLMService(
        llm_adapter
    )

    # =========================================================
    # Database
    # =========================================================

    database_backend = create_database_backend(
        settings
    )

    # =========================================================
    # Patient Service
    # =========================================================

    patient_service = PatientService(
        repository=database_backend.patient
    )

    # =========================================================
    # Graph
    # =========================================================

    return build_triage_graph(
        llm_service=llm_service,
        database_backend=database_backend,
        patient_service=patient_service,
    )