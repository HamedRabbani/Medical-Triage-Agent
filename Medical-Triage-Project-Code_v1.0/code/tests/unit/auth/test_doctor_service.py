from types import SimpleNamespace

from application.auth.authorization_service import AuthorizationService
from application.services.doctor_service import DoctorService


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


def make_uow(doctor=None, can_access=False):

    repository = SimpleNamespace(
        get_by_id=lambda doctor_id: doctor,
        get_by_user_id=lambda user_id: doctor,
        can_access_patient=lambda doctor_id, patient_id: can_access,
    )

    return SimpleNamespace(
        doctors=repository,
    )


def test_doctor_can_get_own_profile():

    doctor = SimpleNamespace(
        doctor_id=10,
        user_id=20,
    )

    user = make_user(
        AuthorizationService.DOCTOR,
        20,
    )

    service = DoctorService(
        make_uow(doctor)
    )

    result = service.get_doctor(
        user,
        10,
    )

    assert result is doctor


def test_doctor_cannot_get_another_doctor_profile():

    doctor = SimpleNamespace(
        doctor_id=10,
        user_id=20,
    )

    user = make_user(
        AuthorizationService.DOCTOR,
        30,
    )

    service = DoctorService(
        make_uow(doctor)
    )

    result = service.get_doctor(
        user,
        10,
    )

    assert result is None


def test_doctor_can_access_assigned_patient():

    user = make_user(
        AuthorizationService.DOCTOR,
        20,
    )

    doctor = SimpleNamespace(
        doctor_id=10,
        user_id=20,
    )

    service = DoctorService(
        make_uow(doctor, can_access=True)
    )

    result = service.can_access_patient(
        user,
        100,
    )

    assert result is True


def test_doctor_cannot_access_unassigned_patient():

    user = make_user(
        AuthorizationService.DOCTOR,
        20,
    )

    doctor = SimpleNamespace(
        doctor_id=10,
        user_id=20,
    )

    service = DoctorService(
        make_uow(doctor, can_access=False)
    )

    result = service.can_access_patient(
        user,
        200,
    )

    assert result is False