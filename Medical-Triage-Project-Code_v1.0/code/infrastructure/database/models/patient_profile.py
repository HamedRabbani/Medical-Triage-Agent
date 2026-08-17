from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .patient_doctor import PatientDoctor
    from .user_account import UserAccount


class PatientProfile(Base):
    __tablename__ = "PatientProfile"

    patient_id: Mapped[int] = mapped_column(
        "PatientId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        "UserId",
        ForeignKey("UserAccount.UserId"),
        nullable=False,
        unique=True,
    )

    first_name: Mapped[str] = mapped_column(
        "FirstName",
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        "LastName",
        String(100),
        nullable=False,
    )

    date_of_birth: Mapped[date] = mapped_column(
        "DateOfBirth",
        Date,
        nullable=False,
    )

    gender: Mapped[str] = mapped_column(
        "Gender",
        String(20),
        nullable=False,
    )

    national_id: Mapped[str] = mapped_column(
        "NationalId",
        String(20),
        nullable=False,
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        nullable=False,
        default=lambda: datetime.now(),
    )

    user: Mapped["UserAccount"] = relationship(
        "UserAccount",
        back_populates="patient_profile",
    )

    doctor_relationships: Mapped[list["PatientDoctor"]] = relationship(
        "PatientDoctor",
        back_populates="patient",
    )