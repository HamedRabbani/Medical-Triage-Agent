from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.doctor_profile import DoctorProfile
from ..models.patient_doctor import PatientDoctor
from .base import BaseRepository


class DoctorRepository(BaseRepository[DoctorProfile]):
    """Repository for doctor persistence operations."""

    def __init__(self, session: Session):
        super().__init__(session, DoctorProfile)

    def get_by_id(
        self,
        doctor_id: int,
    ) -> DoctorProfile | None:
        """Return a doctor by doctor ID."""

        return self.session.get(
            DoctorProfile,
            doctor_id,
        )

    def get_by_user_id(
        self,
        user_id: int,
    ) -> DoctorProfile | None:
        """Return a doctor profile by user ID."""

        statement = select(DoctorProfile).where(
            DoctorProfile.user_id == user_id
        )

        return self.session.scalars(statement).first()

    def can_access_patient(
        self,
        doctor_id: int,
        patient_id: int,
    ) -> bool:
        """Return True if doctor is assigned to the patient."""

        statement = select(PatientDoctor.relation_id).where(
            PatientDoctor.doctor_id == doctor_id,
            PatientDoctor.patient_id == patient_id,
            PatientDoctor.end_date.is_(None),
        )

        return self.session.scalar(statement) is not None