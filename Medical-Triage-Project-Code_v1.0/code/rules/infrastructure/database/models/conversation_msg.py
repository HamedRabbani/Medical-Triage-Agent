from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .triage_session import TriageSession


class ConversationMsg(Base):
    __tablename__ = "ConversationMsg"

    # Primary key
    message_id: Mapped[int] = mapped_column(
        "MessageId",
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

    # Message sender type
    sender_type: Mapped[str] = mapped_column(
        "SenderType",
        String(20),
        nullable=False,
    )

    # Message content
    content: Mapped[str] = mapped_column(
        "Content",
        Text,
        nullable=False,
    )

    # Message timestamp
    timestamp: Mapped[datetime] = mapped_column(
        "Timestamp",
        DateTime,
        nullable=False,
    )

    # Related triage session
    session: Mapped["TriageSession"] = relationship(
        back_populates="messages",
    )