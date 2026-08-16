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


def test_patient_service_patient_can_access_own_profile() -> None:

    with SessionLocal() as session:

        uow = UnitOfWork(session)
        service = PatientService(uow)

        patients = uow.patients.get_all()

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


def test_patient_service_patient_cannot_access_another_patient() -> None:

    with SessionLocal() as session:

        uow = UnitOfWork(session)
        service = PatientService(uow)

        patients = uow.patients.get_all()

        if len(patients) < 2:
            return

        target_patient = patients[1]

        user = make_user(
            AuthorizationService.PATIENT,
            patients[0].user_id,
        )

        result = service.get_patient(
            user,
            target_patient.patient_id,
        )

        assert result is None


def test_patient_service_get_by_user_allows_own_profile() -> None:

    with SessionLocal() as session:

        uow = UnitOfWork(session)
        service = PatientService(uow)

        patients = uow.patients.get_all()

        if not patients:
            return

        patient = patients[0]

        user = make_user(
            AuthorizationService.PATIENT,
            patient.user_id,
        )

        result = service.get_patient_by_user(
            user,
            patient.user_id,
        )

        assert result is not None
        assert result.patient_id == patient.patient_id


def test_patient_service_get_by_user_rejects_another_patient() -> None:

    with SessionLocal() as session:

        uow = UnitOfWork(session)
        service = PatientService(uow)

        patients = uow.patients.get_all()

        if len(patients) < 2:
            return

        current_patient = patients[0]
        target_patient = patients[1]

        user = make_user(
            AuthorizationService.PATIENT,
            current_patient.user_id,
        )

        result = service.get_patient_by_user(
            user,
            target_patient.user_id,
        )

        assert result is None