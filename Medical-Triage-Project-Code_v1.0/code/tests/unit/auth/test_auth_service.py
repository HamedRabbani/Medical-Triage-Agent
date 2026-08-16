from types import SimpleNamespace

from application.auth.auth_service import AuthService
from application.contracts.auth.login_request import LoginRequest


class FakePasswordService:
    @staticmethod
    def verify_password(
        password: str,
        stored_hash: str,
    ) -> bool:
        return (
            password == "CorrectPassword123!"
            and stored_hash == "HASH"
        )


class FakeAuthRepository:
    def __init__(self, user=None):
        self.user = user

    def get_user_by_email(self, email: str):
        return self.user


def create_user(
    status="Active",
    password_hash="HASH",
    role_name="Patient",
    patient_id=10,
    doctor_id=None,
):
    role = SimpleNamespace(
        role_name=role_name,
    )

    user_role = SimpleNamespace(
        role=role,
    )

    patient_profile = None

    if patient_id is not None:
        patient_profile = SimpleNamespace(
            patient_id=patient_id,
        )

    doctor_profile = None

    if doctor_id is not None:
        doctor_profile = SimpleNamespace(
            doctor_id=doctor_id,
        )

    return SimpleNamespace(
        user_id=1,
        email="test@example.com",
        password_hash=password_hash,
        status=status,
        user_roles=[user_role],
        patient_profile=patient_profile,
        doctor_profile=doctor_profile,
    )


def create_service(user):
    repository = FakeAuthRepository(user)

    return AuthService(
        auth_repository=repository,
        password_service=FakePasswordService,
    )


def test_successful_patient_login():
    user = create_user(
        role_name="Patient",
        patient_id=10,
    )

    service = create_service(user)

    request = LoginRequest(
        email="TEST@example.com",
        password="CorrectPassword123!",
    )

    result = service.login(request)

    assert result.success is True
    assert result.user_id == 1
    assert result.email == "test@example.com"
    assert result.role == "Patient"
    assert result.patient_id == 10
    assert result.doctor_id is None


def test_successful_doctor_login():
    user = create_user(
        role_name="Doctor",
        patient_id=None,
        doctor_id=25,
    )

    service = create_service(user)

    request = LoginRequest(
        email="doctor@example.com",
        password="CorrectPassword123!",
    )

    result = service.login(request)

    assert result.success is True
    assert result.role == "Doctor"
    assert result.patient_id is None
    assert result.doctor_id == 25


def test_unknown_email_is_rejected():
    service = create_service(None)

    request = LoginRequest(
        email="unknown@example.com",
        password="CorrectPassword123!",
    )

    result = service.login(request)

    assert result.success is False
    assert result.user_id is None
    assert result.message == (
        "Invalid email or password."
    )


def test_wrong_password_is_rejected():
    user = create_user()

    service = create_service(user)

    request = LoginRequest(
        email="test@example.com",
        password="WrongPassword123!",
    )

    result = service.login(request)

    assert result.success is False
    assert result.user_id is None
    assert result.message == (
        "Invalid email or password."
    )


def test_inactive_account_is_rejected():
    user = create_user(
        status="Disabled",
    )

    service = create_service(user)

    request = LoginRequest(
        email="test@example.com",
        password="CorrectPassword123!",
    )

    result = service.login(request)

    assert result.success is False
    assert result.user_id is None
    assert result.message == (
        "Account is not active."
    )