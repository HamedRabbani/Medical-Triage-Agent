from application.ports.conversation_history_port import (
    ConversationHistoryPort,
)


class SupabaseConversationHistoryRepository(
    ConversationHistoryPort
):
    """Supabase implementation of conversation history storage."""

    def __init__(
        self,
        client,
        table_name: str = "ConversationMsg",
    ):
        self.client = client
        self.table_name = table_name

    def get_history(
        self,
        session_id: int,
    ) -> list[dict]:
        """Return conversation history for a session."""

        response = (
            self.client
            .table(self.table_name)
            .select(
                "MessageId,SessionId,SenderType,Content,Timestamp"
            )
            .eq(
                "SessionId",
                session_id,
            )
            .order(
                "Timestamp",
                desc=False,
            )
            .execute()
        )

        rows = response.data or []

        return [
            {
                "message_id": row["MessageId"],
                "sender_type": row["SenderType"],
                "content": row["Content"],
                "timestamp": row["Timestamp"],
            }
            for row in rows
        ]