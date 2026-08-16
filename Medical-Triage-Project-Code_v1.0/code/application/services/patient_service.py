from application.auth.authorization_service import (
    AuthorizationService,
)

from infrastructure.database.unit_of_work import UnitOfWork


class PatientService:
    """Application service for patient use cases."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_patient(
        self,
        user,
        patient_id: int,
    ):
        """Get a patient by ID after authorization."""

        patient = self.uow.patients.get_by_id(
            patient_id
        )

        if patient is None:
            return None

        if not AuthorizationService.can_access_patient_data(
            user,
            patient_user_id=user.user_id,
            target_patient_user_id=patient.user_id,
        ):
            return None

        return patient

    def get_patient_by_user(
        self,
        user,
        user_id: int,
    ):
        """Get patient profile by user ID after authorization."""

        patient = self.uow.patients.get_by_user_id(
            user_id
        )

        if patient is None:
            return None

        if not AuthorizationService.can_access_patient_data(
            user,
            patient_user_id=user.user_id,
            target_patient_user_id=patient.user_id,
        ):
            return None

        return patient

    def get_patient_by_user_id(
        self,
        user_id: int,
    ):
        """Get patient profile by user ID."""

        return self.uow.patients.get_by_user_id(
            user_id
        )