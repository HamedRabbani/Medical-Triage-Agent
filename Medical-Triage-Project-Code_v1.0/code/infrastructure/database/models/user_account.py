from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class UserAccount(Base):
    __tablename__ = "UserAccount"

    # Primary key
    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Unique user email
    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        nullable=False,
    )

    # Password hash
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Optional phone number
    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # Account status
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Active",
    )

    # Account creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )