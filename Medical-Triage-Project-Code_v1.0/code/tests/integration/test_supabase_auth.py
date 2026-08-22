from application.config.settings import Settings
from infrastructure.auth.supabase_auth_repository import (
    SupabaseAuthRepository,
)

from supabase import create_client


def test_supabase_auth_repository():

    settings = Settings(
        _env_file=".env",
        db_backend="supabase",
    )

    client = create_client(
        settings.supabase_url,
        settings.supabase_key,
    )

    repository = (
        SupabaseAuthRepository(
            client
        )
    )

    result = repository.get_user_by_email(
        "nonexistent@example.com"
    )

    assert result is None