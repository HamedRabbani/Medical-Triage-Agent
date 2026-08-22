from dataclasses import dataclass

from application.auth.password_service import (
    PasswordService,
)
from application.ports.auth_port import AuthPort


@dataclass(frozen=True)
class LoginResult:
    success: bool
    user_id: int | None = None
    email: str | None = None
    roles: tuple[str, ...] = ()
    error: str | None = None


class LoginService:
    """
    Application service responsible for user authentication.

    Authentication persistence is provided through AuthPort,
    so this service is independent of SQL Server or Supabase.
    """

    def __init__(
        self,
        auth_repository: AuthPort,
        password_service: PasswordService,
    ) -> None:
        self._auth_repository = auth_repository
        self._password_service = password_service

    def login(
        self,
        email: str,
        password: str,
    ) -> LoginResult:

        normalized_email = (
            email.strip().lower()
        )

        # -----------------------------------------------------
        # Input validation
        # -----------------------------------------------------

        if not normalized_email or not password:

            return LoginResult(
                success=False,
                error="Invalid email or password.",
            )

        # -----------------------------------------------------
        # Retrieve user
        # -----------------------------------------------------

        user = (
            self._auth_repository
            .get_user_by_email(
                normalized_email
            )
        )

        if user is None:

            return LoginResult(
                success=False,
                error="Invalid email or password.",
            )

        # -----------------------------------------------------
        # Account status
        # -----------------------------------------------------

        if user.status != "Active":

            return LoginResult(
                success=False,
                error="Account is not active.",
            )

        # -----------------------------------------------------
        # Password verification
        # -----------------------------------------------------

        password_valid = (
            self._password_service
            .verify_password(
                password,
                user.password_hash,
            )
        )

        if not password_valid:

            return LoginResult(
                success=False,
                error="Invalid email or password.",
            )

        # -----------------------------------------------------
        # Successful authentication
        # -----------------------------------------------------

        return LoginResult(
            success=True,
            user_id=user.user_id,
            email=user.email,
            roles=tuple(user.roles),
        )