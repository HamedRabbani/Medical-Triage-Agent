from application.config.settings import Settings
from application.ports.database_backend import (
    DatabaseBackend,
)

from infrastructure.database.repositories.sql_conversation_history_repository import (
    SQLConversationHistoryRepository,
)
from infrastructure.database.repositories.sql_triage_persistence_repository import (
    SQLTriagePersistenceRepository,
)
from infrastructure.database.repositories.supabase_conversation_history_repository import (
    SupabaseConversationHistoryRepository,
)
from infrastructure.database.repositories.supabase_triage_persistence_repository import (
    SupabaseTriagePersistenceRepository,
)
from infrastructure.database.session import SessionLocal
from infrastructure.database.unit_of_work import UnitOfWork


def create_database_backend(
    settings: Settings,
) -> DatabaseBackend:
    """Create the configured database backend."""

    backend = (
        settings.db_backend
        .strip()
        .lower()
    )

    if backend == "sqlserver":

        session = SessionLocal()
        uow = UnitOfWork(session)

        triage_repository = (
            SQLTriagePersistenceRepository(uow)
        )

        conversation_repository = (
            SQLConversationHistoryRepository(uow)
        )

        result = DatabaseBackend(
            triage=triage_repository,
            conversation=conversation_repository,
        )

        original_close = result.close

        def close() -> None:
            try:
                original_close()
            finally:
                session.close()

        result.close = close

        return result

    if backend == "supabase":

        if not settings.supabase_url:
            raise ValueError(
                "SUPABASE_URL is required "
                "for Supabase backend."
            )

        if not settings.supabase_key:
            raise ValueError(
                "SUPABASE_KEY is required "
                "for Supabase backend."
            )

        from supabase import create_client

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

        return DatabaseBackend(
            triage=triage_repository,
            conversation=conversation_repository,
        )

    raise ValueError(
        f"Unsupported DB_BACKEND: {settings.db_backend}"
    )