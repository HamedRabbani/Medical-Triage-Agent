from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .doctor_profile import DoctorProfile
    from .patient_profile import PatientProfile


class PatientDoctor(Base):
    __tablename__ = "PatientDoctor"

    relation_id: Mapped[int] = mapped_column(
        "RelationId",
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    patient_id: Mapped[int] = mapped_column(
        "PatientId",
        Integer,
        ForeignKey("PatientProfile.PatientId"),
        nullable=False,
    )

    doctor_id: Mapped[int] = mapped_column(
        "DoctorId",
        Integer,
        ForeignKey("DoctorProfile.DoctorId"),
        nullable=False,
    )

    relationship_type: Mapped[str] = mapped_column(
        "RelationshipType",
        String(50),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        "StartDate",
        Date,
        nullable=False,
    )

    end_date: Mapped[date | None] = mapped_column(
        "EndDate",
        Date,
        nullable=True,
    )

    patient: Mapped["PatientProfile"] = relationship(
        "PatientProfile",
        back_populates="doctor_relationships",
    )

    doctor: Mapped["DoctorProfile"] = relationship(
        "DoctorProfile",
        back_populates="patient_relationships",
    )

    __table_args__ = (
        UniqueConstraint(
            "PatientId",
            "DoctorId",
            name="UQ_PatientDoctor_Patient_Doctor",
        ),
    )