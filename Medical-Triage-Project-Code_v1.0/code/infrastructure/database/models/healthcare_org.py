from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .doctor_profile import DoctorProfile


class HealthcareOrg(Base):
    __tablename__ = "HealthcareOrg"

    # Primary key
    organization_id: Mapped[int] = mapped_column(
        "OrganizationId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Organization name
    name: Mapped[str] = mapped_column(
        "Name",
        String(200),
        nullable=False,
    )

    # Organization type
    type: Mapped[str] = mapped_column(
        "Type",
        String(50),
        nullable=False,
    )

    # Unique license number
    license_number: Mapped[str] = mapped_column(
        "LicenseNumber",
        String(100),
        nullable=False,
        unique=True,
    )

    # Organization address
    address: Mapped[str | None] = mapped_column(
        "Address",
        String(500),
        nullable=True,
    )

    # Related doctors
    doctors: Mapped[list["DoctorProfile"]] = relationship(
        back_populates="organization",
    )