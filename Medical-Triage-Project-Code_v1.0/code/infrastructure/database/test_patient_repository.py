from .repositories.patient_repository import PatientRepository
from .session import SessionLocal


def test_patient_repository() -> None:
    with SessionLocal() as session:

        repository = PatientRepository(session)

        patients = repository.get_all()

        print(f"Total patients: {len(patients)}")

        if patients:
            patient = patients[0]

            print(
                f"Patient: "
                f"{patient.first_name} {patient.last_name}"
            )

            found_patient = repository.get_by_id(
                patient.patient_id
            )

            print(
                f"By ID: "
                f"{found_patient.first_name} "
                f"{found_patient.last_name}"
            )

            found_by_user = repository.get_by_user_id(
                patient.user_id
            )

            print(
                f"By User ID: "
                f"{found_by_user.first_name} "
                f"{found_by_user.last_name}"
            )


if __name__ == "__main__":
    test_patient_repository()