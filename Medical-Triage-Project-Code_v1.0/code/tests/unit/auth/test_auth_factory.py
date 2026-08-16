from unittest.mock import patch

from application.auth.login_service import LoginService
from infrastructure.auth.auth_factory import create_login_service


def test_create_login_service():

    with patch(
        "infrastructure.auth.auth_factory.SessionLocal"
    ) as session_factory:

        session = session_factory.return_value

        login_service, returned_session = (
            create_login_service()
        )

        assert isinstance(
            login_service,
            LoginService,
        )

        assert returned_session is session

        session_factory.assert_called_once()