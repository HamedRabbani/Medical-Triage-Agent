from unittest.mock import Mock

from infrastructure.database.repositories.sql_conversation_history_repository import (
    SQLConversationHistoryRepository,
)
from infrastructure.database.repositories.supabase_conversation_history_repository import (
    SupabaseConversationHistoryRepository,
)


def test_sql_and_supabase_repositories_expose_same_contract():
    sql_uow = Mock()

    sql_repository = SQLConversationHistoryRepository(
        sql_uow
    )

    supabase_client = Mock()

    supabase_repository = (
        SupabaseConversationHistoryRepository(
            supabase_client
        )
    )

    assert hasattr(
        sql_repository,
        "get_history",
    )

    assert hasattr(
        supabase_repository,
        "get_history",
    )