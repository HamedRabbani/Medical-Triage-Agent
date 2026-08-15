from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .user_account import UserAccount


class AuditLog(Base):
    __tablename__ = "AuditLog"

    # Primary key
    audit_id: Mapped[int] = mapped_column(
        "AuditId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # User who performed the action
    user_id: Mapped[int] = mapped_column(
        "UserId",
        ForeignKey("UserAccount.UserId"),
        nullable=False,
    )

    # Action performed
    action: Mapped[str] = mapped_column(
        "Action",
        String(100),
        nullable=False,
    )

    # Entity affected by the action
    entity_name: Mapped[str] = mapped_column(
        "EntityName",
        String(100),
        nullable=False,
    )

    # ID of the affected entity
    entity_id: Mapped[int] = mapped_column(
        "EntityId",
        nullable=False,
    )

    # Previous value
    old_value: Mapped[str | None] = mapped_column(
        "OldValue",
        Text,
        nullable=True,
    )

    # New value
    new_value: Mapped[str | None] = mapped_column(
        "NewValue",
        Text,
        nullable=True,
    )

    # Audit timestamp
    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        nullable=False,
    )

    # Related user
    user: Mapped["UserAccount"] = relationship()