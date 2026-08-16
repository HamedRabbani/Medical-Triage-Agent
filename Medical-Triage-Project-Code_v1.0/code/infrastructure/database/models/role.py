from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


if TYPE_CHECKING:
    from .user_role import UserRole


class Role(Base):
    """
    ORM model representing an application role.

    Examples:
        - Patient
        - Doctor
        - HospitalAdmin
        - SystemAdmin
    """

    __tablename__ = "Role"

    # =========================================================
    # Primary Key
    # =========================================================

    role_id: Mapped[int] = mapped_column(
        "RoleId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # =========================================================
    # Role Information
    # =========================================================

    role_name: Mapped[str] = mapped_column(
        "RoleName",
        String(50),
        unique=True,
        nullable=False,
    )

    # =========================================================
    # Relationships
    # =========================================================

    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole",
        back_populates="role",
    )