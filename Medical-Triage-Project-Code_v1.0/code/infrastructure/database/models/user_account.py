from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


if TYPE_CHECKING:
    from .doctor_profile import DoctorProfile
    from .patient_profile import PatientProfile
    from .user_role import UserRole


class UserAccount(Base):
    """
    ORM model for application user accounts.

    Responsibilities:
        - Store authentication credentials.
        - Store account status.
        - Provide relationships to roles and domain profiles.

    Authentication passwords must always be stored as hashes.
    Plain-text passwords must never be persisted.
    """

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
    # Authentication
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

    # =========================================================
    # Contact Information
    # =========================================================

    phone: Mapped[str | None] = mapped_column(
        "Phone",
        String(20),
        nullable=True,
    )

    # =========================================================
    # Account Status
    # =========================================================

    status: Mapped[str] = mapped_column(
        "Status",
        String(20),
        nullable=False,
        default="Active",
    )

    # =========================================================
    # Audit
    # =========================================================

    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    # =========================================================
    # Relationships
    # =========================================================

    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    patient_profile: Mapped["PatientProfile | None"] = relationship(
        "PatientProfile",
        back_populates="user",
        uselist=False,
    )

    doctor_profile: Mapped["DoctorProfile | None"] = relationship(
        "DoctorProfile",
        back_populates="user",
        uselist=False,
    )

