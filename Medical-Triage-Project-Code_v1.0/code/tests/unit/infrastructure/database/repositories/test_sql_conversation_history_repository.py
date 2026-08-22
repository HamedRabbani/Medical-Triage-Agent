from unittest.mock import Mock

from infrastructure.database.repositories.sql_conversation_history_repository import (
    SQLConversationHistoryRepository,
)


def test_get_history_maps_messages():
    uow = Mock()

    message_1 = Mock(
        message_id=1,
        sender_type="Patient",
        content="I have chest pain.",
        timestamp=None,
    )

    message_2 = Mock(
        message_id=2,
        sender_type="Patient",
        content="It started 30 minutes ago.",
        timestamp=None,
    )

    uow.triage.get_messages.return_value = [
        message_1,
        message_2,
    ]

    repository = SQLConversationHistoryRepository(
        uow
    )

    result = repository.get_history(
        session_id=10
    )

    assert result == [
        {
            "message_id": 1,
            "sender_type": "Patient",
            "content": "I have chest pain.",
            "timestamp": None,
        },
        {
            "message_id": 2,
            "sender_type": "Patient",
            "content": "It started 30 minutes ago.",
            "timestamp": None,
        },
    ]

    uow.triage.get_messages.assert_called_once_with(
        10
    )