from .repositories.medical_record_repository import (
    MedicalRecordRepository,
)
from .session import SessionLocal


def test_medical_record_repository() -> None:
    with SessionLocal() as session:

        repository = MedicalRecordRepository(session)

        records = repository.get_all()

        print(f"Total medical records: {len(records)}")

        if records:
            record = records[0]

            print(f"Record ID: {record.record_id}")
            print(f"Condition: {record.condition}")

            patient_records = repository.get_by_patient_id(
                record.patient_id
            )

            print(
                f"Patient records: "
                f"{len(patient_records)}"
            )

            verified_records = (
                repository.get_verified_by_patient_id(
                    record.patient_id
                )
            )

            print(
                f"Verified records: "
                f"{len(verified_records)}"
            )


if __name__ == "__main__":
    test_medical_record_repository()