from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    String,
    UnicodeText,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .triage_session import TriageSession


class ConversationMsg(Base):
    __tablename__ = "ConversationMsg"

    message_id: Mapped[int] = mapped_column(
        "MessageId",
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    session_id: Mapped[int] = mapped_column(
        "SessionId",
        BigInteger,
        ForeignKey("TriageSession.SessionId"),
        nullable=False,
    )

    sender_type: Mapped[str] = mapped_column(
        "SenderType",
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        "Content",
        UnicodeText,
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        "Timestamp",
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    session: Mapped["TriageSession"] = relationship(
        "TriageSession",
        back_populates="messages",
    )