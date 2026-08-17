from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .patient_profile import PatientProfile
    from .user_account import UserAccount
    from .verification_status import VerificationStatus


class MedicalRecord(Base):
    __tablename__ = "MedicalRecord"

    record_id: Mapped[int] = mapped_column(
        "RecordId",
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    patient_id: Mapped[int] = mapped_column(
        "PatientId",
        Integer,
        ForeignKey("PatientProfile.PatientId"),
        nullable=False,
    )

    created_by_user_id: Mapped[int] = mapped_column(
        "CreatedByUserId",
        Integer,
        ForeignKey("UserAccount.UserId"),
        nullable=False,
    )

    condition: Mapped[str] = mapped_column(
        "Condition",
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        "Description",
        Text,
        nullable=True,
    )

    record_type: Mapped[str] = mapped_column(
        "RecordType",
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    verification_status_id: Mapped[int] = mapped_column(
        "VerificationStatusId",
        Integer,
        ForeignKey("VerificationStatus.StatusId"),
        nullable=False,
    )

    patient: Mapped["PatientProfile"] = relationship(
        "PatientProfile",
    )

    created_by_user: Mapped["UserAccount"] = relationship(
        "UserAccount",
    )

    verification_status: Mapped["VerificationStatus"] = relationship(
        "VerificationStatus",
    )