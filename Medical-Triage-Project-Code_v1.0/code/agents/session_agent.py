from application.services.conversation_service import (
    ConversationService,
)
from application.services.short_term_memory_service import (
    ShortTermMemoryService,
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
    """Create/reuse session, persist message and load memory."""

    patient_id = state.get("patient_id")
    session_id = state.get("session_id")
    user_message = state.get("user_message")

    if patient_id is None:
        raise ValueError("patient_id is required.")

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

    memory_service = ShortTermMemoryService()

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

    agent_service.add_message(
        session_id=session_id,
        content=user_message,
        sender_type="Patient",
    )

    database_backend.triage.commit()

    history = conversation_service.get_history(
        session_id
    )

    short_term_memory = memory_service.load(
        session_id=session_id,
        history=history,
    )

    return {
        **state,
        "session_id": session_id,
        "conversation_history": (
            short_term_memory.recent_messages
        ),
        "short_term_memory": short_term_memory,
    }