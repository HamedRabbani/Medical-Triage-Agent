from infrastructure.database.unit_of_work import UnitOfWork
from application.ports.conversation_history_port import (
    ConversationHistoryPort,
)


class SQLConversationHistoryRepository(
    ConversationHistoryPort
):
    """SQL Server implementation of conversation history storage."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

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
                "sender_type": message.sender_type,
                "content": message.content,
                "timestamp": message.timestamp,
            }
            for message in messages
        ]