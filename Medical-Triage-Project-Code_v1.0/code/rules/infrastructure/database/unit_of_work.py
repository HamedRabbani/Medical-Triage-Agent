from sqlalchemy.orm import Session

from .repositories.user_repository import UserRepository
from .repositories.patient_repository import PatientRepository
from .repositories.medical_record_repository import (
    MedicalRecordRepository,
)
from .repositories.triage_repository import TriageRepository
from .repositories.doctor_repository import DoctorRepository


class UnitOfWork:
    """Manage repositories and database transactions."""

    def __init__(self, session: Session):
        self.session = session

        self.users = UserRepository(session)
        self.patients = PatientRepository(session)
        self.doctors = DoctorRepository(session)
        self.medical_records = MedicalRecordRepository(session)
        self.triage = TriageRepository(session)

    def commit(self) -> None:
        """Commit the current transaction."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self.session.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()

        return False