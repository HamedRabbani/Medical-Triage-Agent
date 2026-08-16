from application.auth.authentication_session import (
    AuthenticationSession,
)


def test_authenticated_session():

    session = AuthenticationSession(
        user_id=10,
        email="doctor@example.com",
        roles=("Doctor",),
    )

    assert session.is_authenticated is True
    assert session.user_id == 10
    assert session.email == "doctor@example.com"
    assert session.roles == ("Doctor",)


def test_session_has_role():

    session = AuthenticationSession(
        user_id=10,
        email="doctor@example.com",
        roles=("Doctor",),
    )

    assert session.has_role("Doctor") is True
    assert session.has_role("Patient") is False


def test_session_has_any_role():

    session = AuthenticationSession(
        user_id=10,
        email="doctor@example.com",
        roles=("Doctor",),
    )

    assert session.has_any_role(
        ["Patient", "Doctor"]
    ) is True


def test_session_rejects_unknown_roles():

    session = AuthenticationSession(
        user_id=10,
        email="doctor@example.com",
        roles=("Patient",),
    )

    assert session.has_any_role(
        ["Doctor", "SystemAdmin"]
    ) is False