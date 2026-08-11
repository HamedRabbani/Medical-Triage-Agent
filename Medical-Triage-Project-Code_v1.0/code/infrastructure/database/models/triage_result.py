from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from ..base import Base

if TYPE_CHECKING:
    from .triage_session import TriageSession


class TriageResult(Base):
    __tablename__ = "TriageResult"

    # Primary key
    result_id: Mapped[int] = mapped_column(
        "ResultId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Triage session reference
    session_id: Mapped[int] = mapped_column(
        "SessionId",
        ForeignKey("TriageSession.SessionId"),
        nullable=False,
    )

    # Risk classification
    risk_level: Mapped[str] = mapped_column(
        "RiskLevel",
        String(20),
        nullable=False,
    )

    # Model confidence score
    confidence_score: Mapped[float] = mapped_column(
        "ConfidenceScore",
        Numeric(5, 2),
        nullable=False,
    )

    # Recommended action
    recommendation: Mapped[str] = mapped_column(
        "Recommendation",
        Text,
        nullable=False,
    )

    # Result creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        nullable=False,
    )

    # Related triage session
    session: Mapped["TriageSession"] = relationship(
        back_populates="results",
    )