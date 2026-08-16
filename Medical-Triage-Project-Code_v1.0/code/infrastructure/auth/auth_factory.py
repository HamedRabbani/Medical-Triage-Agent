from infrastructure.database.session import SessionLocal

from infrastructure.auth.auth_repository import AuthRepository

from application.auth.login_service import LoginService
from application.auth.password_service import PasswordService


def create_login_service():

    session = SessionLocal()

    repository = AuthRepository(
        session
    )

    password_service = PasswordService()

    service = LoginService(
        auth_repository=repository,
        password_service=password_service,
    )

    return service, session