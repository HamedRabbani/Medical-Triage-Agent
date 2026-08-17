from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .role import Role
    from .user_account import UserAccount


class UserRole(Base):
    __tablename__ = "UserRole"

    user_role_id: Mapped[int] = mapped_column(
        "UserRoleId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        "UserId",
        Integer,
        ForeignKey("UserAccount.UserId"),
        nullable=False,
    )

    role_id: Mapped[int] = mapped_column(
        "RoleId",
        Integer,
        ForeignKey("Role.RoleId"),
        nullable=False,
    )

    user: Mapped["UserAccount"] = relationship(
        "UserAccount",
        back_populates="user_roles",
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="user_roles",
    )

    __table_args__ = (
        UniqueConstraint(
            "UserId",
            "RoleId",
            name="UQ_UserRole_User_Role",
        ),
    )