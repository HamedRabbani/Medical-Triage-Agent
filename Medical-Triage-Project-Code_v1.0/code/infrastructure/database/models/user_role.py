from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class UserRole(Base):
    __tablename__ = "UserRole"

    # Primary key
    user_role_id: Mapped[int] = mapped_column(
        "UserRoleId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Foreign key to UserAccount
    user_id: Mapped[int] = mapped_column(
        "UserId",
        ForeignKey("UserAccount.UserId"),
        nullable=False,
    )

    # Foreign key to Role
    role_id: Mapped[int] = mapped_column(
        "RoleId",
        ForeignKey("Role.RoleId"),
        nullable=False,
    )

    # Related user
    user: Mapped["UserAccount"] = relationship(
        back_populates="user_roles",
    )

    # Related role
    role: Mapped["Role"] = relationship(
        back_populates="user_roles",
    )

    # Prevent duplicate user-role assignments
    __table_args__ = (
        UniqueConstraint(
            "UserId",
            "RoleId",
            name="UQ_UserRole_User_Role",
        ),
    )