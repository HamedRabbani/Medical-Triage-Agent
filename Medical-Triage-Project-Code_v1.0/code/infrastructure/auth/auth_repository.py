from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from infrastructure.database.models.user_account import UserAccount
from infrastructure.database.models.user_role import UserRole


class AuthRepository:
    """
    Data-access layer for authentication.

    Responsibilities:
        - Retrieve user account by email.
        - Load authentication-related roles.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(
        self,
        email: str,
    ) -> UserAccount | None:
        """
        Retrieve a user account by email with roles loaded.
        """

        statement = (
            select(UserAccount)
            .options(
                selectinload(
                    UserAccount.user_roles
                ).selectinload(
                    UserRole.role
                )
            )
            .where(
                UserAccount.email == email
            )
        )

        return self.session.scalar(statement)