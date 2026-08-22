from datetime import datetime, timezone

from application.ports.conversation_persistence_port import (
    ConversationPersistencePort,
)


class SupabaseConversationPersistenceRepository(
    ConversationPersistencePort
):
    """Supabase implementation of conversation persistence."""

    def __init__(
        self,
        client,
        session_table: str = "TriageSession",
        message_table: str = "ConversationMsg",
    ):
        self.client = client
        self.session_table = session_table
        self.message_table = message_table

    def create_session(
        self,
        patient_id: int,
    ) -> int:

        response = (
            self.client
            .table(self.session_table)
            .insert(
                {
                    "PatientId": patient_id,
                    "StartTime": datetime.now(
                        timezone.utc
                    ).isoformat(),
                    "Status": "Active",
                }
            )
            .execute()
        )

        rows = response.data or []

        if not rows:
            raise RuntimeError(
                "Supabase did not return the created session."
            )

        return rows[0]["SessionId"]

    def add_message(
        self,
        session_id: int,
        content: str,
        sender_type: str = "Patient",
    ) -> dict:

        response = (
            self.client
            .table(self.message_table)
            .insert(
                {
                    "SessionId": session_id,
                    "SenderType": sender_type,
                    "Content": content,
                    "Timestamp": datetime.now(
                        timezone.utc
                    ).isoformat(),
                }
            )
            .execute()
        )

        rows = response.data or []

        if not rows:
            raise RuntimeError(
                "Supabase did not return the created message."
            )

        row = rows[0]

        return {
            "message_id": row["MessageId"],
            "session_id": row["SessionId"],
            "sender_type": row["SenderType"],
            "content": row["Content"],
            "timestamp": row["Timestamp"],
        }

    def get_history(
        self,
        session_id: int,
    ) -> list[dict]:

        response = (
            self.client
            .table(self.message_table)
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
                "session_id": row["SessionId"],
                "sender_type": row["SenderType"],
                "content": row["Content"],
                "timestamp": row["Timestamp"],
            }
            for row in rows
        ]