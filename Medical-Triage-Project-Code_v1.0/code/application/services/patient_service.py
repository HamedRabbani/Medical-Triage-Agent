from application.auth.authorization_service import (
    AuthorizationService,
)

from application.ports.patient_port import PatientPort


class PatientService:
    """Application service for patient use cases."""

    def __init__(
        self,
        repository: PatientPort,
    ):
        self.repository = repository

    def get_patient(
        self,
        user,
        patient_id: int,
    ):
        """Get patient by patient ID after authorization."""

        patient = self.repository.get_patient_by_id(
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
        """Get patient by user ID after authorization."""

        patient = self.repository.get_patient_by_user_id(
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
        """Get patient by user ID."""

        return self.repository.get_patient_by_user_id(
            user_id
        )