from types import SimpleNamespace

from application.auth.authorization_service import (
    AuthorizationService,
)
from application.services.patient_service import PatientService
from infrastructure.database.session import SessionLocal
from infrastructure.database.unit_of_work import UnitOfWork


def make_user(role: str, user_id: int):
    return SimpleNamespace(
        user_id=user_id,
        user_roles=[
            SimpleNamespace(
                role=SimpleNamespace(
                    role_name=role,
                ),
            )
        ],
    )


def test_patient_service() -> None:
    with SessionLocal() as session:

        uow = UnitOfWork(session)
        service = PatientService(uow)

        patients = uow.patients.get_all()

        print(f"Total patients: {len(patients)}")

        if not patients:
            return

        patient = patients[0]

        user = make_user(
            AuthorizationService.PATIENT,
            patient.user_id,
        )

        result = service.get_patient(
            user,
            patient.patient_id,
        )

        assert result is not None
        assert result.patient_id == patient.patient_id

        patient_by_user = service.get_patient_by_user(
            user,
            patient.user_id,
        )

        assert patient_by_user is not None
        assert patient_by_user.patient_id == patient.patient_id

        print(
            f"Patient: "
            f"{result.first_name} "
            f"{result.last_name}"
        )

        print("Patient service test passed.")


if __name__ == "__main__":
    test_patient_service()