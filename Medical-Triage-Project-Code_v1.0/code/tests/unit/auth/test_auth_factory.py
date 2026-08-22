from unittest.mock import Mock, patch

from application.config.settings import Settings
from infrastructure.auth.auth_factory import (
    create_login_service,
)
from infrastructure.auth.sql_auth_repository import (
    SQLAuthRepository,
)


def test_create_login_service():

    fake_session = Mock()

    settings = Settings(
        db_backend="sqlserver",
    )

    with patch(
        "infrastructure.database.session.SessionLocal",
        return_value=fake_session,
    ) as session_factory:

        service, session = create_login_service(
            settings
        )

    session_factory.assert_called_once()

    assert session is fake_session
    assert service is not None

    assert (
        service._auth_repository.__class__
        is SQLAuthRepository
    )