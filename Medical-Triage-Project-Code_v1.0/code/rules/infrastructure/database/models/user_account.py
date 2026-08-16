from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


if TYPE_CHECKING:
    from .user_role import UserRole
    from .patient_profile import PatientProfile
    from .doctor_profile import DoctorProfile


class UserAccount(Base):
    __tablename__ = "UserAccount"

    # =========================================================
    # Primary Key
    # =========================================================

    user_id: Mapped[int] = mapped_column(
        "UserId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # =========================================================
    # Account Information
    # =========================================================

    email: Mapped[str] = mapped_column(
        "Email",
        String(254),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        "PasswordHash",
        String(255),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        "Phone",
        String(20),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        "Status",
        String(20),
        nullable=False,
        default="Active",
    )

    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        nullable=False,
        server_default=text("SYSUTCDATETIME()"),
    )

    # =========================================================
    # Relationships
    # =========================================================

    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole",
        back_populates="user",
    )

    patient_profile: Mapped[
        "PatientProfile | None"
    ] = relationship(
        "PatientProfile",
        back_populates="user",
        uselist=False,
    )

    doctor_profile: Mapped[
        "DoctorProfile | None"
    ] = relationship(
        "DoctorProfile",
        back_populates="user",
        uselist=False,
    )