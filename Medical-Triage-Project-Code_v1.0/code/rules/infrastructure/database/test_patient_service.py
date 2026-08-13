from infrastructure.database.session import SessionLocal
from infrastructure.database.unit_of_work import UnitOfWork
from application.services.patient_service import PatientService


def test_patient_service() -> None:
    with SessionLocal() as session:

        uow = UnitOfWork(session)
        service = PatientService(uow)

        patients = uow.patients.get_all()

        print(f"Total patients: {len(patients)}")

        if patients:
            patient = service.get_patient(
                patients[0].patient_id
            )

            print(
                f"Patient: "
                f"{patient.first_name} "
                f"{patient.last_name}"
            )

            patient_by_user = service.get_patient_by_user(
                patient.user_id
            )

            print(
                f"Patient by user: "
                f"{patient_by_user.first_name} "
                f"{patient_by_user.last_name}"
            )

        print("Patient service test passed.")


if __name__ == "__main__":
    test_patient_service()