from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .user_account import UserAccount
    from .patient_doctor import PatientDoctor


class PatientProfile(Base):
    __tablename__ = "PatientProfile"

    # Primary key
    patient_id: Mapped[int] = mapped_column(
        "PatientId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # One-to-one relation with UserAccount
    user_id: Mapped[int] = mapped_column(
        "UserId",
        ForeignKey("UserAccount.UserId"),
        nullable=False,
        unique=True,
    )

    # Patient first name
    first_name: Mapped[str] = mapped_column(
        "FirstName",
        String(100),
        nullable=False,
    )

    # Patient last name
    last_name: Mapped[str] = mapped_column(
        "LastName",
        String(100),
        nullable=False,
    )

    # Patient date of birth
    date_of_birth: Mapped[datetime] = mapped_column(
        "DateOfBirth",
        DateTime,
        nullable=False,
    )

    # Patient gender
    gender: Mapped[str] = mapped_column(
        "Gender",
        String(20),
        nullable=False,
    )

    # National identification number
    national_id: Mapped[str] = mapped_column(
        "NationalId",
        String(20),
        nullable=False,
        unique=True,
    )

    # Profile creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        nullable=False,
    )

    # Related user account
    user: Mapped["UserAccount"] = relationship(
        back_populates="patient_profile",
    )

    # Doctor relationships
    doctor_relationships: Mapped[list["PatientDoctor"]] = relationship(
        back_populates="patient",
    )