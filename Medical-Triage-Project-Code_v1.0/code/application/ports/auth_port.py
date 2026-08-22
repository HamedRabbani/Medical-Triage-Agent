from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AuthUser:
    user_id: int
    email: str
    password_hash: str
    status: str
    roles: tuple[str, ...]


class AuthPort(Protocol):

    def get_user_by_email(
        self,
        email: str,
    ) -> AuthUser | None:
        ...