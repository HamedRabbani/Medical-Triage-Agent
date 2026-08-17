from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .healthcare_org import HealthcareOrg
    from .patient_doctor import PatientDoctor
    from .user_account import UserAccount


class DoctorProfile(Base):
    __tablename__ = "DoctorProfile"

    doctor_id: Mapped[int] = mapped_column(
        "DoctorId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        "UserId",
        ForeignKey("UserAccount.UserId"),
        nullable=False,
        unique=True,
    )

    organization_id: Mapped[int] = mapped_column(
        "OrganizationId",
        ForeignKey("HealthcareOrg.OrganizationId"),
        nullable=False,
    )

    license_number: Mapped[str] = mapped_column(
        "LicenseNumber",
        String(100),
        nullable=False,
        unique=True,
    )

    specialty: Mapped[str] = mapped_column(
        "Specialty",
        String(100),
        nullable=False,
    )

    user: Mapped["UserAccount"] = relationship(
        "UserAccount",
        back_populates="doctor_profile",
    )

    organization: Mapped["HealthcareOrg"] = relationship(
        "HealthcareOrg",
        back_populates="doctors",
    )

    patient_relationships: Mapped[list["PatientDoctor"]] = relationship(
        "PatientDoctor",
        back_populates="doctor",
    )