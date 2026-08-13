from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.user_account import UserAccount
from .base import BaseRepository


class UserRepository(BaseRepository[UserAccount]):
    """Repository for UserAccount persistence operations."""

    def __init__(self, session: Session):
        super().__init__(session, UserAccount)

    def get_by_email(self, email: str) -> UserAccount | None:
        """Return a user by email."""
        statement = select(UserAccount).where(
            UserAccount.email == email
        )

        return self.session.scalars(statement).first()