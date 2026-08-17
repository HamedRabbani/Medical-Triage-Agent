from dataclasses import dataclass

from application.auth.password_service import PasswordService
from infrastructure.auth.auth_repository import AuthRepository


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
    """

    def __init__(
        self,
        auth_repository: AuthRepository,
        password_service: PasswordService,
    ) -> None:
        self._auth_repository = auth_repository
        self._password_service = password_service

    def login(
        self,
        email: str,
        password: str,
    ) -> LoginResult:

        normalized_email = email.strip().lower()

        if not normalized_email or not password:
            return LoginResult(
                success=False,
                error="Invalid email or password.",
            )

        user = self._auth_repository.get_user_by_email(
            normalized_email
        )

        if user is None:
            return LoginResult(
                success=False,
                error="Invalid email or password.",
            )

        # DEBUG - remove after testing
        print("EMAIL:", user.email)
        print("HASH:", user.password_hash)
        print(
            "VERIFY:",
            self._password_service.verify_password(
                password,
                user.password_hash,
            )
        )

        if user.status != "Active":
            return LoginResult(
                success=False,
                error="Account is not active.",
            )

        password_valid = self._password_service.verify_password(
            password,
            user.password_hash,
        )

        if not password_valid:
            return LoginResult(
                success=False,
                error="Invalid email or password.",
            )

        roles = tuple(
            sorted(
                {
                    assignment.role.role_name
                    for assignment in user.user_roles
                    if assignment.role is not None
                }
            )
        )

        return LoginResult(
            success=True,
            user_id=user.user_id,
            email=user.email,
            roles=roles,
        )