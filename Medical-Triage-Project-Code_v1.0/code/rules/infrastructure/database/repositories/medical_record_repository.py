from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.medical_record import MedicalRecord
from .base import BaseRepository


class MedicalRecordRepository(BaseRepository[MedicalRecord]):
    """Repository for medical record persistence operations."""

    def __init__(self, session: Session):
        super().__init__(session, MedicalRecord)

    def get_by_patient_id(
        self,
        patient_id: int,
    ) -> list[MedicalRecord]:
        """Return all medical records for a patient."""

        statement = (
            select(MedicalRecord)
            .where(MedicalRecord.patient_id == patient_id)
            .order_by(MedicalRecord.created_at.desc())
        )

        return list(self.session.scalars(statement).all())

    def get_verified_by_patient_id(
        self,
        patient_id: int,
    ) -> list[MedicalRecord]:
        """Return verified medical records for a patient."""

        statement = (
            select(MedicalRecord)
            .join(MedicalRecord.verification_status)
            .where(
                MedicalRecord.patient_id == patient_id,
                MedicalRecord.verification_status.has(
                    status_name="Verified"
                ),
            )
            .order_by(MedicalRecord.created_at.desc())
        )

        return list(self.session.scalars(statement).all())