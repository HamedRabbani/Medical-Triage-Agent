from infrastructure.database.unit_of_work import UnitOfWork


class PatientService:
    """Application service for patient use cases."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_patient(self, patient_id: int):
        """Get a patient by ID."""
        return self.uow.patients.get_by_id(patient_id)

    def get_patient_by_user(self, user_id: int):
        """Get patient profile by user ID."""
        return self.uow.patients.get_by_user_id(user_id)