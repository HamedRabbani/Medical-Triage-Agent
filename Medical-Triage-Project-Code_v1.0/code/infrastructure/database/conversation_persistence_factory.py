from application.config.settings import Settings
from application.ports.database_backend import (
    DatabaseBackend,
)


def create_database_backend(
    settings: Settings,
) -> DatabaseBackend:

    backend = (
        settings.db_backend
        .strip()
        .lower()
    )

    if backend == "sqlserver":

        from infrastructure.database.repositories.sql_conversation_history_repository import (
            SQLConversationHistoryRepository,
        )
        from infrastructure.database.repositories.sql_patient_repository import (
            SQLPatientRepository,
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

        backend = DatabaseBackend(
            triage=SQLTriagePersistenceRepository(
                uow
            ),
            conversation=SQLConversationHistoryRepository(
                uow
            ),
            patient=SQLPatientRepository(
                uow
            ),
        )

        backend.close = session.close

        return backend

    if backend == "supabase":

        if not settings.supabase_url:
            raise ValueError(
                "SUPABASE_URL is required."
            )

        if not settings.supabase_key:
            raise ValueError(
                "SUPABASE_KEY is required."
            )

        from supabase import create_client

        from infrastructure.database.repositories.supabase_conversation_history_repository import (
            SupabaseConversationHistoryRepository,
        )
        from infrastructure.database.repositories.supabase_patient_repository import (
            SupabasePatientRepository,
        )
        from infrastructure.database.repositories.supabase_triage_persistence_repository import (
            SupabaseTriagePersistenceRepository,
        )

        client = create_client(
            settings.supabase_url,
            settings.supabase_key,
        )

        return DatabaseBackend(
            triage=SupabaseTriagePersistenceRepository(
                client
            ),
            conversation=SupabaseConversationHistoryRepository(
                client
            ),
            patient=SupabasePatientRepository(
                client
            ),
        )

    raise ValueError(
        f"Unsupported DB_BACKEND: {settings.db_backend}"
    )