from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticationSession:
    """
    Represents the authenticated application session.

    This object contains only authentication-related identity data.

    It does not contain:
        - passwords
        - password hashes
        - database sessions
        - SQLAlchemy objects
    """

    user_id: int
    email: str
    roles: tuple[str, ...]

    @property
    def is_authenticated(self) -> bool:
        return True

    def has_role(self, role_name: str) -> bool:
        return role_name in self.roles

    def has_any_role(
        self,
        role_names: list[str],
    ) -> bool:
        return any(
            role in self.roles
            for role in role_names
        )