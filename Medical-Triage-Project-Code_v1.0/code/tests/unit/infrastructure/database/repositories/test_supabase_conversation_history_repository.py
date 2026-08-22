from unittest.mock import Mock

from infrastructure.database.repositories.supabase_conversation_history_repository import (
    SupabaseConversationHistoryRepository,
)


def test_get_history_returns_mapped_messages():
    client = Mock()

    query = client.table.return_value
    query.select.return_value = query
    query.eq.return_value = query
    query.order.return_value = query

    query.execute.return_value = Mock(
        data=[
            {
                "MessageId": 1,
                "SessionId": 10,
                "SenderType": "Patient",
                "Content": "I have chest pain.",
                "Timestamp": "2026-08-22T10:00:00",
            },
            {
                "MessageId": 2,
                "SessionId": 10,
                "SenderType": "Patient",
                "Content": "It started 30 minutes ago.",
                "Timestamp": "2026-08-22T10:01:00",
            },
        ]
    )

    repository = SupabaseConversationHistoryRepository(
        client
    )

    result = repository.get_history(
        session_id=10
    )

    assert result == [
        {
            "message_id": 1,
            "sender_type": "Patient",
            "content": "I have chest pain.",
            "timestamp": "2026-08-22T10:00:00",
        },
        {
            "message_id": 2,
            "sender_type": "Patient",
            "content": "It started 30 minutes ago.",
            "timestamp": "2026-08-22T10:01:00",
        },
    ]

    client.table.assert_called_once_with(
        "ConversationMsg"
    )

    query.eq.assert_called_once_with(
        "SessionId",
        10,
    )

    query.order.assert_called_once_with(
        "Timestamp",
        desc=False,
    )