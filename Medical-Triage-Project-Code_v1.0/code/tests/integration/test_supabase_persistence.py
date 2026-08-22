from application.config.settings import Settings

from infrastructure.database.repositories.supabase_triage_persistence_repository import (
    SupabaseTriagePersistenceRepository,
)
from infrastructure.database.repositories.supabase_conversation_history_repository import (
    SupabaseConversationHistoryRepository,
)

from supabase import create_client


def test_supabase_connectivity_and_read():
    settings = Settings(
        _env_file=".env",
    )

    assert settings.supabase_url
    assert settings.supabase_key

    client = create_client(
        settings.supabase_url,
        settings.supabase_key,
    )

    triage_repository = (
        SupabaseTriagePersistenceRepository(
            client
        )
    )

    conversation_repository = (
        SupabaseConversationHistoryRepository(
            client
        )
    )

    # ---------------------------------------------------------
    # Read-only verification
    # ---------------------------------------------------------

    patient_exists = (
        triage_repository.patient_exists(2)
    )

    assert isinstance(
        patient_exists,
        bool,
    )

    history = (
        conversation_repository.get_history(
            1
        )
    )

    assert isinstance(
        history,
        list,
    )