from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .user_account import UserAccount
    from .healthcare_org import HealthcareOrg
    from .patient_doctor import PatientDoctor


class DoctorProfile(Base):
    __tablename__ = "DoctorProfile"

    # Primary key
    doctor_id: Mapped[int] = mapped_column(
        "DoctorId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # One-to-one relation with UserAccount
    user_id: Mapped[int] = mapped_column(
        "UserId",
        ForeignKey("UserAccount.UserId"),
        nullable=False,
        unique=True,
    )

    # Doctor's organization
    organization_id: Mapped[int] = mapped_column(
        "OrganizationId",
        ForeignKey("HealthcareOrg.OrganizationId"),
        nullable=False,
    )

    # Medical license number
    license_number: Mapped[str] = mapped_column(
        "LicenseNumber",
        String(100),
        nullable=False,
        unique=True,
    )

    # Medical specialty
    specialty: Mapped[str] = mapped_column(
        "Specialty",
        String(100),
        nullable=False,
    )

    # Related user account
    user: Mapped["UserAccount"] = relationship(
        back_populates="doctor_profile",
    )

    # Related healthcare organization
    organization: Mapped["HealthcareOrg"] = relationship(
        back_populates="doctors",
    )

    # Patient relationships
    patient_relationships: Mapped[list["PatientDoctor"]] = relationship(
        back_populates="doctor",
    )