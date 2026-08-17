from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .user_account import UserAccount


class AuditLog(Base):
    __tablename__ = "AuditLog"

    audit_id: Mapped[int] = mapped_column(
        "AuditId",
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int | None] = mapped_column(
        "UserId",
        Integer,
        ForeignKey("UserAccount.UserId"),
        nullable=True,
    )

    action: Mapped[str] = mapped_column(
        "Action",
        String(50),
        nullable=False,
    )

    entity_name: Mapped[str] = mapped_column(
        "EntityName",
        String(100),
        nullable=False,
    )

    entity_id: Mapped[int | None] = mapped_column(
        "EntityId",
        Integer,
        nullable=True,
    )

    old_value: Mapped[str | None] = mapped_column(
        "OldValue",
        Text,
        nullable=True,
    )

    new_value: Mapped[str | None] = mapped_column(
        "NewValue",
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    user: Mapped["UserAccount | None"] = relationship(
        "UserAccount",
    )