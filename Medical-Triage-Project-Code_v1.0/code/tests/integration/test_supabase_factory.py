from application.config.settings import Settings

from infrastructure.database.conversation_persistence_factory import (
    create_database_backend,
)


def test_supabase_factory_real_backend():
    settings = Settings(
        _env_file=".env",
        db_backend="supabase",
    )

    backend = create_database_backend(
        settings
    )

    try:
        assert (
            backend.triage.__class__.__name__
            == "SupabaseTriagePersistenceRepository"
        )

        assert (
            backend.conversation.__class__.__name__
            == "SupabaseConversationHistoryRepository"
        )

    finally:
        backend.close()