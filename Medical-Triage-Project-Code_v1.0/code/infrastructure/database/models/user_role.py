from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


if TYPE_CHECKING:
    from .role import Role
    from .user_account import UserAccount


class UserRole(Base):
    """
    Association model between UserAccount and Role.

    A user can have multiple roles and a role can belong
    to multiple users.
    """

    __tablename__ = "UserRole"

    # =========================================================
    # Primary Key
    # =========================================================

    user_role_id: Mapped[int] = mapped_column(
        "UserRoleId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # =========================================================
    # Foreign Keys
    # =========================================================

    user_id: Mapped[int] = mapped_column(
        "UserId",
        ForeignKey("UserAccount.UserId"),
        nullable=False,
    )

    role_id: Mapped[int] = mapped_column(
        "RoleId",
        ForeignKey("Role.RoleId"),
        nullable=False,
    )

    # =========================================================
    # Relationships
    # =========================================================

    user: Mapped["UserAccount"] = relationship(
        "UserAccount",
        back_populates="user_roles",
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="user_roles",
    )

    # =========================================================
    # Constraints
    # =========================================================

    __table_args__ = (
        UniqueConstraint(
            "UserId",
            "RoleId",
            name="UQ_UserRole_User_Role",
        ),
    )