from infrastructure.database.unit_of_work import UnitOfWork


class ConversationService:
    """Application service for conversation history."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_history(
        self,
        session_id: int,
    ) -> list[dict]:
        """Return conversation history for a triage session."""

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