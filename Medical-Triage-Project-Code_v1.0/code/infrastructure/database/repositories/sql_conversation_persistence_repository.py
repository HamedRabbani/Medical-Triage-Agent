from datetime import UTC, datetime

from infrastructure.database.models.conversation_msg import (
    ConversationMsg,
)
from infrastructure.database.models.triage_session import (
    TriageSession,
)
from infrastructure.database.unit_of_work import UnitOfWork

from application.ports.conversation_persistence_port import (
    ConversationPersistencePort,
)


class SQLConversationPersistenceRepository(
    ConversationPersistencePort
):
    """SQL Server implementation of conversation persistence."""

    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow

    def create_session(
        self,
        patient_id: int,
    ) -> int:
        triage_session = TriageSession(
            patient_id=patient_id,
            start_time=datetime.now(UTC),
            status="Active",
        )

        self.uow.triage.add(
            triage_session
        )

        self.uow.commit()

        return triage_session.session_id

    def add_message(
        self,
        session_id: int,
        content: str,
        sender_type: str = "Patient",
    ) -> dict:

        message = ConversationMsg(
            session_id=session_id,
            sender_type=sender_type,
            content=content,
            timestamp=datetime.now(UTC),
        )

        self.uow.triage.add_message(
            message
        )

        self.uow.commit()

        return {
            "message_id": message.message_id,
            "session_id": message.session_id,
            "sender_type": message.sender_type,
            "content": message.content,
            "timestamp": message.timestamp,
        }

    def get_history(
        self,
        session_id: int,
    ) -> list[dict]:

        messages = self.uow.triage.get_messages(
            session_id
        )

        return [
            {
                "message_id": message.message_id,
                "session_id": message.session_id,
                "sender_type": message.sender_type,
                "content": message.content,
                "timestamp": message.timestamp,
            }
            for message in messages
        ]