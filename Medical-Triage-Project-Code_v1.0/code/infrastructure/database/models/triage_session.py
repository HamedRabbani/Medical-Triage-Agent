from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .conversation_msg import ConversationMsg
    from .patient_profile import PatientProfile
    from .triage_result import TriageResult


class TriageSession(Base):
    __tablename__ = "TriageSession"

    session_id: Mapped[int] = mapped_column(
        "SessionId",
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    patient_id: Mapped[int] = mapped_column(
        "PatientId",
        ForeignKey("PatientProfile.PatientId"),
        nullable=False,
    )

    start_time: Mapped[datetime] = mapped_column(
        "StartTime",
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    end_time: Mapped[datetime | None] = mapped_column(
        "EndTime",
        DateTime,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        "Status",
        String(20),
        nullable=False,
        default="Active",
    )

    patient: Mapped["PatientProfile"] = relationship(
        "PatientProfile",
    )

    messages: Mapped[list["ConversationMsg"]] = relationship(
        "ConversationMsg",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    result: Mapped["TriageResult | None"] = relationship(
        "TriageResult",
        back_populates="session",
        uselist=False,
        cascade="all, delete-orphan",
    )