from sqlalchemy.orm import Session

from application.auth.login_service import LoginService
from application.auth.password_service import PasswordService
from infrastructure.auth.auth_repository import AuthRepository


def create_login_service(
    session: Session,
) -> LoginService:
    """
    Compose the authentication application service.

    Infrastructure dependencies are injected here so that
    LoginService remains independent from SQLAlchemy session
    construction.
    """

    auth_repository = AuthRepository(
        session=session,
    )

    password_service = PasswordService()

    return LoginService(
        auth_repository=auth_repository,
        password_service=password_service,
    )