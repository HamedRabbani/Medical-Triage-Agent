from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.patient_profile import PatientProfile
from .base import BaseRepository


class PatientRepository(BaseRepository[PatientProfile]):
    """Repository for patient persistence operations."""

    def __init__(self, session: Session):
        super().__init__(session, PatientProfile)

    def get_by_user_id(
        self,
        user_id: int,
    ) -> PatientProfile | None:
        """Return a patient profile by user ID."""

        statement = select(PatientProfile).where(
            PatientProfile.user_id == user_id
        )

        return self.session.scalars(statement).first()