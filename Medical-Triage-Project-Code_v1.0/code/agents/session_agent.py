from infrastructure.database.session import SessionLocal
from infrastructure.database.unit_of_work import UnitOfWork

from application.services.triage_service import TriageService
from application.services.triage_agent_service import TriageAgentService
from application.services.conversation_service import ConversationService

from application.services.short_term_memory_service import (
    ShortTermMemoryService,
)


def session_agent(state):
    """Create or reuse triage session, save user message,
    and load conversation history.
    """

    patient_id = state.get("patient_id")
    session_id = state.get("session_id")
    user_message = state.get("user_message")

    if patient_id is None:
        raise ValueError("patient_id is required.")

    if not user_message:
        return state

    with SessionLocal() as session:

        uow = UnitOfWork(session)

        triage_service = TriageService(uow)

        agent_service = TriageAgentService(
            triage_service
        )

        conversation_service = ConversationService(
            uow
        )
        memory_service = ShortTermMemoryService(
        conversation_service
        )

        # -------------------------
        # 1. Create or reuse session
        # -------------------------

        if session_id is None:

            triage_session = (
                agent_service.create_session(
                    patient_id
                )
            )

            session_id = triage_session.session_id

        # -------------------------
        # 2. Save current message
        # -------------------------

        agent_service.add_message(
            session_id=session_id,
            content=user_message,
            sender_type="Patient",
        )

        # -------------------------
        # 3. Load conversation history
        # -------------------------

        short_term_memory = memory_service.load(
        session_id
        )

    # -------------------------
    # 4. Update LangGraph State
    # -------------------------

    return {
        **state,
        "session_id": session_id,
        "conversation_history": short_term_memory.recent_messages,
        "short_term_memory": short_term_memory,
    }