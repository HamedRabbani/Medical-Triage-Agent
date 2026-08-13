from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .patient_profile import PatientProfile
    from .conversation_msg import ConversationMsg
    from .triage_result import TriageResult


class TriageSession(Base):
    __tablename__ = "TriageSession"

    # Primary key
    session_id: Mapped[int] = mapped_column(
        "SessionId",
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

    # Session start time
    start_time: Mapped[datetime] = mapped_column(
        "StartTime",
        DateTime,
        nullable=False,
    )

    # Session end time
    end_time: Mapped[datetime | None] = mapped_column(
        "EndTime",
        DateTime,
        nullable=True,
    )

    # Session status
    status: Mapped[str] = mapped_column(
        "Status",
        String(20),
        nullable=False,
    )

    # Related patient
    patient: Mapped["PatientProfile"] = relationship()

    # Conversation messages
    messages: Mapped[list["ConversationMsg"]] = relationship(
        back_populates="session",
    )

    # Triage results
    results: Mapped[list["TriageResult"]] = relationship(
        back_populates="session",
    )