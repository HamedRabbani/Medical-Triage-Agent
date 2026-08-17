from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .triage_session import TriageSession


class TriageResult(Base):
    __tablename__ = "TriageResult"

    result_id: Mapped[int] = mapped_column(
        "ResultId",
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    session_id: Mapped[int] = mapped_column(
        "SessionId",
        BigInteger,
        ForeignKey("TriageSession.SessionId"),
        nullable=False,
        unique=True,
    )

    risk_level: Mapped[str] = mapped_column(
        "RiskLevel",
        String(20),
        nullable=False,
    )

    confidence_score: Mapped[float] = mapped_column(
        "ConfidenceScore",
        Numeric(5, 2),
        nullable=False,
    )

    recommendation: Mapped[str] = mapped_column(
        "Recommendation",
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    session: Mapped["TriageSession"] = relationship(
        "TriageSession",
        back_populates="result",
        uselist=False,
    )