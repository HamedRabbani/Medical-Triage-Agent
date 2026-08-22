from application.ports.patient_port import PatientPort

from infrastructure.database.unit_of_work import UnitOfWork


class SQLPatientRepository(PatientPort):
    """SQL Server implementation of patient persistence."""

    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow

    def get_patient_by_id(
        self,
        patient_id: int,
    ):
        return self.uow.patients.get_by_id(
            patient_id
        )

    def get_patient_by_user_id(
        self,
        user_id: int,
    ):
        return self.uow.patients.get_by_user_id(
            user_id
        )