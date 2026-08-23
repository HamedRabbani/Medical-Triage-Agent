from application.services.conversation_service import (
    ConversationService,
)

from application.services.memory_service import (
    MemoryService,
)

from application.services.triage_agent_service import (
    TriageAgentService,
)

from application.services.triage_service import (
    TriageService,
)


def session_agent(
    state,
    database_backend,
):
    """
    Create/reuse session, persist message and load memory.
    """

    patient_id = state.get(
        "patient_id"
    )

    session_id = state.get(
        "session_id"
    )

    user_message = state.get(
        "user_message"
    )

    if patient_id is None:
        raise ValueError(
            "patient_id is required."
        )

    if not user_message:
        return state

    triage_service = TriageService(
        database_backend.triage
    )

    agent_service = TriageAgentService(
        triage_service
    )

    conversation_service = ConversationService(
        database_backend.conversation
    )

    memory_service = MemoryService(
        patient_repository=database_backend.patient,
        medical_record_repository=database_backend.medical_record,
        triage_repository=database_backend.triage,
    )

    # =========================================================
    # Load patient information
    # =========================================================

    patient = (
        database_backend.patient
        .get_patient_by_id(
            patient_id
        )
    )

    user_id = None

    if patient is not None:
        user_id = patient.user_id

    # =========================================================
    # Create / reuse session
    # =========================================================

    if session_id is None:

        triage_session = (
            agent_service.create_session(
                patient_id
            )
        )

        database_backend.triage.commit()

        session_id = (
            triage_session.session_id
        )

    # =========================================================
    # Persist user message
    # =========================================================

    agent_service.add_message(
        session_id=session_id,
        content=user_message,
        sender_type="Patient",
    )

    database_backend.triage.commit()

    # =========================================================
    # Load conversation history
    # =========================================================

    history = conversation_service.get_history(
        session_id
    )

    # =========================================================
    # Retrieve memory
    # =========================================================

    memory_context = memory_service.retrieve(
        patient_id=patient_id,
        session_id=session_id,
        history=history,
    )

    # =========================================================
    # Return updated state
    # =========================================================

    return {
        **state,

        "patient_id": patient_id,

        "user_id": user_id,

        "session_id": session_id,

        "conversation_history": (
            memory_context
            .short_term
            .recent_messages
        ),

        "short_term_memory": (
            memory_context
            .short_term
        ),

        "memory_context": memory_context,
    }