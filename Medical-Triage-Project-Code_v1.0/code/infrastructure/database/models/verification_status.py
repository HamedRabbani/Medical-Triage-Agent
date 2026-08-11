from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class VerificationStatus(Base):
    __tablename__ = "VerificationStatus"

    # Primary key
    status_id: Mapped[int] = mapped_column(
        "StatusId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Verification status name
    status_name: Mapped[str] = mapped_column(
        "StatusName",
        String(50),
        unique=True,
        nullable=False,
    )