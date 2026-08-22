from unittest.mock import Mock

from infrastructure.database.repositories.sql_conversation_persistence_repository import (
    SQLConversationPersistenceRepository,
)
from infrastructure.database.repositories.supabase_conversation_persistence_repository import (
    SupabaseConversationPersistenceRepository,
)


def test_sql_repository_exposes_conversation_contract():
    repository = SQLConversationPersistenceRepository(
        Mock()
    )

    assert callable(repository.create_session)
    assert callable(repository.add_message)
    assert callable(repository.get_history)


def test_supabase_repository_exposes_conversation_contract():
    repository = (
        SupabaseConversationPersistenceRepository(
            Mock()
        )
    )

    assert callable(repository.create_session)
    assert callable(repository.add_message)
    assert callable(repository.get_history)