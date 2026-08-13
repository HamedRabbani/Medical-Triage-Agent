from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .patient_profile import PatientProfile
    from .user_account import UserAccount
    from .verification_status import VerificationStatus


class MedicalRecord(Base):
    __tablename__ = "MedicalRecord"

    # Primary key
    record_id: Mapped[int] = mapped_column(
        "RecordId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Patient reference
    patient_id: Mapped[int] = mapped_column(
        "PatientId",
        ForeignKey("PatientProfile.PatientId"),
        nullable=False,
    )

    # User who created the record
    created_by_user_id: Mapped[int] = mapped_column(
        "CreatedByUserId",
        ForeignKey("UserAccount.UserId"),
        nullable=False,
    )

    # Medical condition
    condition: Mapped[str] = mapped_column(
        "Condition",
        String(200),
        nullable=False,
    )

    # Medical description
    description: Mapped[str | None] = mapped_column(
        "Description",
        Text,
        nullable=True,
    )

    # Type of medical record
    record_type: Mapped[str] = mapped_column(
        "RecordType",
        String(50),
        nullable=False,
    )

    # Record creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        nullable=False,
    )

    # Verification status reference
    verification_status_id: Mapped[int] = mapped_column(
        "VerificationStatusId",
        ForeignKey("VerificationStatus.StatusId"),
        nullable=False,
    )

    # Related patient
    patient: Mapped["PatientProfile"] = relationship()

    # User who created the record
    created_by_user: Mapped["UserAccount"] = relationship()

    # Verification status
    verification_status: Mapped["VerificationStatus"] = relationship()