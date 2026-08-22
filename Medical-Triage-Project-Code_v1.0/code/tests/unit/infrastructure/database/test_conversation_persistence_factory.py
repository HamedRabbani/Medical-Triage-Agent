from unittest.mock import Mock, patch

from application.config.settings import Settings
from application.ports.database_backend import (
    DatabaseBackend,
)

from infrastructure.database.conversation_persistence_factory import (
    create_database_backend,
)


def test_factory_selects_sqlserver_backend():
    settings = Settings(
        db_backend="sqlserver",
    )

    backend = create_database_backend(
        settings
    )

    try:
        assert isinstance(
            backend,
            DatabaseBackend,
        )

        assert backend.triage is not None
        assert backend.conversation is not None

        assert (
            backend.triage.__class__.__name__
            == "SQLTriagePersistenceRepository"
        )

        assert (
            backend.conversation.__class__.__name__
            == "SQLConversationHistoryRepository"
        )

    finally:
        backend.close()


@patch(
    "supabase.create_client"
)
def test_factory_selects_supabase_backend(
    mock_create_client,
):
    fake_client = Mock()

    mock_create_client.return_value = (
        fake_client
    )

    settings = Settings(
        db_backend="supabase",
        supabase_url=(
            "https://example.supabase.co"
        ),
        supabase_key="test-key",
    )

    backend = create_database_backend(
        settings
    )

    assert isinstance(
        backend,
        DatabaseBackend,
    )

    assert (
        backend.triage.__class__.__name__
        == "SupabaseTriagePersistenceRepository"
    )

    assert (
        backend.conversation.__class__.__name__
        == "SupabaseConversationHistoryRepository"
    )

    mock_create_client.assert_called_once_with(
        "https://example.supabase.co",
        "test-key",
    )


def test_factory_rejects_unknown_backend():
    settings = Settings(
        db_backend="unknown",
    )

    try:
        create_database_backend(
            settings
        )
        assert False

    except ValueError as exc:

        assert (
            "Unsupported DB_BACKEND"
            in str(exc)
        )