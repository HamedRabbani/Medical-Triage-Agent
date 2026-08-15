from datetime import datetime, UTC

from sqlalchemy import DateTime, Integer, String, text

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .user_role import UserRole


from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .patient_profile import PatientProfile
    from .doctor_profile import DoctorProfile

class UserAccount(Base):
    __tablename__ = "UserAccount"

    # Primary key
    user_id: Mapped[int] = mapped_column(
        "UserId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Unique user email
    email: Mapped[str] = mapped_column(
        "Email",
        String(254),
        unique=True,
        nullable=False,
    )

    # Password hash
    password_hash: Mapped[str] = mapped_column(
        "PasswordHash",
        String(255),
        nullable=False,
    )

    # Optional phone number
    phone: Mapped[str | None] = mapped_column(
        "Phone",
        String(20),
        nullable=True,
    )

    # Account status
    status: Mapped[str] = mapped_column(
        "Status",
        String(20),
        nullable=False,
        default="Active",
    )

    # Account creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        nullable=False,
        server_default=text("SYSUTCDATETIME()"),
    )
     
     # Related user-role assignments
    user_roles: Mapped[list["UserRole"]] = relationship(
        back_populates="user",
    )

        # One-to-one patient profile
    patient_profile: Mapped["PatientProfile | None"] = relationship(
        back_populates="user",
        uselist=False,
    )

    # One-to-one doctor profile
    doctor_profile: Mapped["DoctorProfile | None"] = relationship(
        back_populates="user",
        uselist=False,
    )