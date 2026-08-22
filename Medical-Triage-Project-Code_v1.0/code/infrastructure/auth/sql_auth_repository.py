from application.ports.auth_port import AuthUser
from infrastructure.auth.auth_repository import (
    AuthRepository,
)


class SQLAuthRepository:
    """SQL Server implementation of AuthPort."""

    def __init__(
        self,
        repository: AuthRepository,
    ):
        self.repository = repository

    def get_user_by_email(
        self,
        email: str,
    ) -> AuthUser | None:

        user = (
            self.repository
            .get_user_by_email(email)
        )

        if user is None:
            return None

        roles = tuple(
            sorted(
                {
                    assignment.role.role_name
                    for assignment in user.user_roles
                    if assignment.role is not None
                }
            )
        )

        return AuthUser(
            user_id=user.user_id,
            email=user.email,
            password_hash=user.password_hash,
            status=user.status,
            roles=roles,
        )