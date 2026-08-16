from application.auth.authorization_service import (
    AuthorizationService,
)
from infrastructure.database.unit_of_work import UnitOfWork


class MedicalRecordService:
    """Application service for medical record use cases."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    # =========================================================
    # Get Single Medical Record
    # =========================================================

    def get_record(
        self,
        user,
        record_id: int,
    ):
        """
        Return a medical record only if the authenticated
        user is authorized to access it.
        """

        if user is None:
            return None

        record = self.uow.medical_records.get_by_id(
            record_id
        )

        if record is None:
            return None

        # -----------------------------------------------------
        # Patient
        # -----------------------------------------------------

        if AuthorizationService.has_role(
            user,
            AuthorizationService.PATIENT,
        ):
            patient = self.uow.patients.get_by_id(
                record.patient_id
            )

            if patient is None:
                return None

            if patient.user_id != user.user_id:
                return None

            return record

        # -----------------------------------------------------
        # Doctor
        # -----------------------------------------------------

        if AuthorizationService.has_role(
            user,
            AuthorizationService.DOCTOR,
        ):
            doctor = self.uow.doctors.get_by_user_id(
                user.user_id
            )

            if doctor is None:
                return None

            if not self.uow.doctors.can_access_patient(
                doctor.doctor_id,
                record.patient_id,
            ):
                return None

            return record

        # -----------------------------------------------------
        # System Admin
        # -----------------------------------------------------

        if AuthorizationService.has_role(
            user,
            AuthorizationService.SYSTEM_ADMIN,
        ):
            return record

        # -----------------------------------------------------
        # Hospital Admin
        # -----------------------------------------------------

        # HospitalAdmin does NOT currently have unrestricted
        # access to medical records.
        if AuthorizationService.has_role(
            user,
            AuthorizationService.HOSPITAL_ADMIN,
        ):
            return None

        return None

    # =========================================================
    # Get Patient Medical Records
    # =========================================================

    def get_patient_records(
        self,
        user,
        patient_id: int,
    ):
        """
        Return medical records for a patient only if the
        authenticated user is authorized to access them.
        """

        if user is None:
            return []

        # -----------------------------------------------------
        # Patient
        # -----------------------------------------------------

        if AuthorizationService.has_role(
            user,
            AuthorizationService.PATIENT,
        ):
            patient = self.uow.patients.get_by_id(
                patient_id
            )

            if patient is None:
                return []

            if patient.user_id != user.user_id:
                return []

            return self.uow.medical_records.get_by_patient_id(
                patient_id
            )

        # -----------------------------------------------------
        # Doctor
        # -----------------------------------------------------

        if AuthorizationService.has_role(
            user,
            AuthorizationService.DOCTOR,
        ):
            doctor = self.uow.doctors.get_by_user_id(
                user.user_id
            )

            if doctor is None:
                return []

            if not self.uow.doctors.can_access_patient(
                doctor.doctor_id,
                patient_id,
            ):
                return []

            return self.uow.medical_records.get_by_patient_id(
                patient_id
            )

        # -----------------------------------------------------
        # System Admin
        # -----------------------------------------------------

        if AuthorizationService.has_role(
            user,
            AuthorizationService.SYSTEM_ADMIN,
        ):
            return self.uow.medical_records.get_by_patient_id(
                patient_id
            )

        # -----------------------------------------------------
        # Hospital Admin
        # -----------------------------------------------------

        if AuthorizationService.has_role(
            user,
            AuthorizationService.HOSPITAL_ADMIN,
        ):
            return []

        return []