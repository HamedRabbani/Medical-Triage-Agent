from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Role(Base):
    __tablename__ = "Role"

    # Primary key
    role_id: Mapped[int] = mapped_column(
        "RoleId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Unique role name
    role_name: Mapped[str] = mapped_column(
        "RoleName",
        String(50),
        unique=True,
        nullable=False,
    )

    # Related user-role assignments
    user_roles: Mapped[list["UserRole"]] = relationship(
        back_populates="role",
    )