from types import SimpleNamespace

from application.auth.authorization_service import (
    AuthorizationService,
)


def make_user(*roles: str):

    return SimpleNamespace(
        user_roles=[
            SimpleNamespace(
                role=SimpleNamespace(
                    role_name=role,
                ),
            )
            for role in roles
        ]
    )


def test_user_has_role():

    user = make_user("Patient")

    assert AuthorizationService.has_role(
        user,
        "Patient",
    )


def test_user_does_not_have_role():

    user = make_user("Patient")

    assert not AuthorizationService.has_role(
        user,
        "Doctor",
    )


def test_user_can_have_multiple_roles():

    user = make_user(
        "Patient",
        "Doctor",
    )

    assert AuthorizationService.has_role(
        user,
        "Patient",
    )

    assert AuthorizationService.has_role(
        user,
        "Doctor",
    )


def test_has_any_role():

    user = make_user("Doctor")

    assert AuthorizationService.has_any_role(
        user,
        [
            "Patient",
            "Doctor",
        ],
    )


def test_patient_can_access_patient_data():

    user = make_user("Patient")

    assert AuthorizationService.can_access_patient_data(
        user
    )


def test_patient_cannot_manage_patient_data():

    user = make_user("Patient")

    assert not AuthorizationService.can_manage_patient_data(
        user
    )


def test_doctor_can_manage_patient_data():

    user = make_user("Doctor")

    assert AuthorizationService.can_manage_patient_data(
        user
    )


def test_system_admin_can_manage_users():

    user = make_user("SystemAdmin")

    assert AuthorizationService.can_manage_users(
        user
    )


def test_only_system_admin_can_manage_roles():

    doctor = make_user("Doctor")
    admin = make_user("SystemAdmin")

    assert not AuthorizationService.can_manage_roles(
        doctor
    )

    assert AuthorizationService.can_manage_roles(
        admin
    )