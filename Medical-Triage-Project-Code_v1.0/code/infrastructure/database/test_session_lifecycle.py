from infrastructure.database.session import SessionLocal
from infrastructure.database.unit_of_work import UnitOfWork

from application.services.triage_service import TriageService
from application.services.triage_agent_service import TriageAgentService


def test_session_lifecycle():

    print("Starting session lifecycle test...")

    with SessionLocal() as session:

        uow = UnitOfWork(session)

        triage_service = TriageService(uow)

        agent_service = TriageAgentService(
            triage_service
        )

        patient_id = 2

        # -------------------------
        # 1. Create Session
        # -------------------------

        triage_session = agent_service.create_session(
            patient_id
        )

        session_id = triage_session.session_id

        print(
            f"Created Session ID: {session_id}"
        )

        # -------------------------
        # 2. Add first message
        # -------------------------

        message_1 = agent_service.add_message(
            session_id=session_id,
            content="I have chest pain.",
            sender_type="Patient",
        )

        print(
            f"Message 1 ID: {message_1.message_id}"
        )

        # -------------------------
        # 3. Add second message
        # -------------------------

        message_2 = agent_service.add_message(
            session_id=session_id,
            content="It started 30 minutes ago.",
            sender_type="Patient",
        )

        print(
            f"Message 2 ID: {message_2.message_id}"
        )

        # -------------------------
        # 4. Read messages
        # -------------------------

        messages = uow.triage.get_messages(
            session_id
        )

        print(
            f"Total messages: {len(messages)}"
        )

        # -------------------------
        # 5. Assertions
        # -------------------------

        assert len(messages) >= 2

        assert (
            messages[-2].session_id
            == session_id
        )

        assert (
            messages[-1].session_id
            == session_id
        )

        assert (
            messages[-2].content
            == "I have chest pain."
        )

        assert (
            messages[-1].content
            == "It started 30 minutes ago."
        )

        print(
            "Session lifecycle test PASSED."
        )


if __name__ == "__main__":
    test_session_lifecycle()