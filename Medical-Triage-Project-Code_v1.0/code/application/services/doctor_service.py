from application.auth.authorization_service import (
    AuthorizationService,
)
from infrastructure.database.unit_of_work import UnitOfWork


class DoctorService:
    """Application service for doctor use cases."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_doctor(
        self,
        user,
        doctor_id: int,
    ):
        """
        Return doctor profile only if the authenticated
        user owns that doctor profile.
        """

        if not AuthorizationService.has_role(
            user,
            AuthorizationService.DOCTOR,
        ):
            return None

        doctor = self.uow.doctors.get_by_id(
            doctor_id
        )

        if doctor is None:
            return None

        if doctor.user_id != user.user_id:
            return None

        return doctor

    def can_access_patient(
        self,
        user,
        patient_id: int,
    ) -> bool:
        """
        Return True only if the authenticated doctor
        is assigned to the requested patient.
        """

        if not AuthorizationService.has_role(
            user,
            AuthorizationService.DOCTOR,
        ):
            return False

        doctor = self.uow.doctors.get_by_user_id(
            user.user_id
        )

        if doctor is None:
            return False

        return self.uow.doctors.can_access_patient(
            doctor.doctor_id,
            patient_id,
        )