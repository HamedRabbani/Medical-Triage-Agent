from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .patient_profile import PatientProfile
    from .doctor_profile import DoctorProfile


class PatientDoctor(Base):
    __tablename__ = "PatientDoctor"

    # Primary key
    relation_id: Mapped[int] = mapped_column(
        "RelationId",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Foreign key to PatientProfile
    patient_id: Mapped[int] = mapped_column(
        "PatientId",
        ForeignKey("PatientProfile.PatientId"),
        nullable=False,
    )

    # Foreign key to DoctorProfile
    doctor_id: Mapped[int] = mapped_column(
        "DoctorId",
        ForeignKey("DoctorProfile.DoctorId"),
        nullable=False,
    )

    # Relationship type
    relationship_type: Mapped[str] = mapped_column(
        "RelationshipType",
        String(50),
        nullable=False,
    )

    # Relationship start date
    start_date: Mapped[date] = mapped_column(
        "StartDate",
        Date,
        nullable=False,
    )

    # Relationship end date
    end_date: Mapped[date | None] = mapped_column(
        "EndDate",
        Date,
        nullable=True,
    )

    # Related patient
    patient: Mapped["PatientProfile"] = relationship(
        back_populates="doctor_relationships",
    )

    # Related doctor
    doctor: Mapped["DoctorProfile"] = relationship(
        back_populates="patient_relationships",
    )