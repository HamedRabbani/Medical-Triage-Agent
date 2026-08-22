from application.config.settings import (
    Settings,
)
from application.auth.login_service import (
    LoginService,
)
from application.auth.password_service import (
    PasswordService,
)

from infrastructure.auth.sql_auth_repository import (
    SQLAuthRepository,
)


def create_login_service(
    settings: Settings | None = None,
):

    if settings is None:
        settings = Settings()

    backend = (
        settings.db_backend
        .strip()
        .lower()
    )

    password_service = PasswordService()

    # =========================================================
    # SQL Server
    # =========================================================

    if backend == "sqlserver":

        from infrastructure.database.session import (
            SessionLocal,
        )

        from infrastructure.auth.auth_repository import (
            AuthRepository,
        )

        session = SessionLocal()

        repository = AuthRepository(
            session
        )

        auth_repository = SQLAuthRepository(
            repository
        )

        service = LoginService(
            auth_repository=auth_repository,
            password_service=password_service,
        )

        return service, session

    # =========================================================
    # Supabase
    # =========================================================

    if backend == "supabase":

        if not settings.supabase_url:
            raise ValueError(
                "SUPABASE_URL is required."
            )

        if not settings.supabase_key:
            raise ValueError(
                "SUPABASE_KEY is required."
            )

        from supabase import (
            create_client,
        )

        from infrastructure.auth.supabase_auth_repository import (
            SupabaseAuthRepository,
        )

        client = create_client(
            settings.supabase_url,
            settings.supabase_key,
        )

        auth_repository = (
            SupabaseAuthRepository(
                client
            )
        )

        service = LoginService(
            auth_repository=auth_repository,
            password_service=password_service,
        )

        return service, None

    raise ValueError(
        f"Unsupported DB_BACKEND: "
        f"{settings.db_backend}"
    )