from typing import Protocol


class PatientPort(Protocol):

    def get_patient_by_id(
        self,
        patient_id: int,
    ):
        ...

    def get_patient_by_user_id(
        self,
        user_id: int,
    ):
        ...