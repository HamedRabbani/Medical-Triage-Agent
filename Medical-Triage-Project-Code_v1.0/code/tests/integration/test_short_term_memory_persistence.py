from infrastructure.database.session import SessionLocal
from infrastructure.database.unit_of_work import UnitOfWork
from infrastructure.database.repositories.sql_conversation_history_repository import (
    SQLConversationHistoryRepository,
)

from application.services.triage_service import TriageService
from application.services.triage_agent_service import (
    TriageAgentService,
)
from application.services.conversation_service import (
    ConversationService,
)
from application.services.short_term_memory_service import (
    ShortTermMemoryService,
)

from infrastructure.database.repositories.sql_triage_persistence_repository import (
    SQLTriagePersistenceRepository,
)

def test_short_term_memory_reconstructed_from_database():
    with SessionLocal() as session:

        uow = UnitOfWork(session)

        persistence = SQLTriagePersistenceRepository(uow)

        triage_service = TriageService(
            persistence
        )

        agent_service = TriageAgentService(
            triage_service
        )

        history_repository = (
            SQLConversationHistoryRepository(uow)
        )

        conversation_service = ConversationService(
            history_repository
        )

        memory_service = ShortTermMemoryService()

        patient_id = 2

        # -----------------------------------------------------
        # 1. Create session
        # -----------------------------------------------------

        triage_session = agent_service.create_session(
            patient_id
        )

        session_id = triage_session.session_id

        # -----------------------------------------------------
        # 2. Persist conversation messages
        # -----------------------------------------------------

        agent_service.add_message(
            session_id=session_id,
            content="I have chest pain.",
            sender_type="Patient",
        )

        agent_service.add_message(
            session_id=session_id,
            content="It started 30 minutes ago.",
            sender_type="Patient",
        )

        # -----------------------------------------------------
        # 3. Read persisted conversation
        # -----------------------------------------------------

        history = conversation_service.get_history(
            session_id
        )

        assert len(history) >= 2

        assert history[-2]["content"] == (
            "I have chest pain."
        )

        assert history[-1]["content"] == (
            "It started 30 minutes ago."
        )

        # -----------------------------------------------------
        # 4. Reconstruct Short-Term Memory
        # -----------------------------------------------------

        memory = memory_service.load(
            session_id=session_id,
            history=history,
        )

        # -----------------------------------------------------
        # 5. Verify reconstruction
        # -----------------------------------------------------

        assert memory.session_id == session_id

        assert memory.recent_messages == history

        assert memory.medical_context.symptoms == []

        assert memory.medical_context.age is None

        assert memory.medical_context.severity is None

        assert memory.medical_context.duration is None

        assert memory.medical_context.red_flags == []