from application.config.settings import Settings
from application.ports.database_backend import (
    DatabaseBackend,
)


def create_database_backend(
    settings: Settings,
) -> DatabaseBackend:
    """Create the configured database backend."""

    backend = (
        settings.db_backend
        .strip()
        .lower()
    )

    # =========================================================
    # SQL Server
    # =========================================================

    if backend == "sqlserver":

        # IMPORTANT:
        # Import SQL Server dependencies only when
        # SQL Server is actually selected.
        from infrastructure.database.repositories.sql_conversation_history_repository import (
            SQLConversationHistoryRepository,
        )
        from infrastructure.database.repositories.sql_triage_persistence_repository import (
            SQLTriagePersistenceRepository,
        )
        from infrastructure.database.session import (
            SessionLocal,
        )
        from infrastructure.database.unit_of_work import (
            UnitOfWork,
        )

        session = SessionLocal()
        uow = UnitOfWork(session)

        triage_repository = (
            SQLTriagePersistenceRepository(
                uow
            )
        )

        conversation_repository = (
            SQLConversationHistoryRepository(
                uow
            )
        )

        backend_resource = session

        database_backend = DatabaseBackend(
            triage=triage_repository,
            conversation=conversation_repository,
        )

        def close() -> None:
            backend_resource.close()

        database_backend.close = close

        return database_backend

    # =========================================================
    # Supabase
    # =========================================================

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

        from infrastructure.database.repositories.supabase_conversation_history_repository import (
            SupabaseConversationHistoryRepository,
        )
        from infrastructure.database.repositories.supabase_triage_persistence_repository import (
            SupabaseTriagePersistenceRepository,
        )

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
        f"Unsupported DB_BACKEND: "
        f"{settings.db_backend}"
    )