from typing import Protocol


class MedicalRecordPort(Protocol):

    def get_by_patient_id(
        self,
        patient_id: int,
    ) -> list:
        ...