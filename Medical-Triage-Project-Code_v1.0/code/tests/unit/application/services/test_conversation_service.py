from unittest.mock import Mock

from application.services.conversation_service import (
    ConversationService,
)


def test_get_history_uses_repository():
    repository = Mock()

    expected_history = [
        {
            "message_id": 1,
            "sender_type": "Patient",
            "content": "I have chest pain.",
            "timestamp": None,
        }
    ]

    repository.get_history.return_value = expected_history

    service = ConversationService(
        repository
    )

    result = service.get_history(
        session_id=10
    )

    assert result == expected_history

    repository.get_history.assert_called_once_with(
        10
    )