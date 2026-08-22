from application.auth.login_service import LoginService
from application.ports.auth_port import AuthUser


class FakePasswordService:

    def __init__(self, valid: bool = True):
        self.valid = valid

    def verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        return self.valid


class FakeAuthRepository:

    def __init__(self, user: AuthUser | None = None):
        self.user = user
        self.requested_email = None

    def get_user_by_email(
        self,
        email: str,
    ) -> AuthUser | None:
        self.requested_email = email
        return self.user


def make_user(
    *,
    user_id=1,
    email="test@example.com",
    password_hash="HASH",
    status="Active",
    roles=("Patient",),
) -> AuthUser:

    return AuthUser(
        user_id=user_id,
        email=email,
        password_hash=password_hash,
        status=status,
        roles=tuple(roles),
    )


def test_login_success():
    user = make_user()

    repository = FakeAuthRepository(user)
    password_service = FakePasswordService(
        valid=True
    )

    service = LoginService(
        auth_repository=repository,
        password_service=password_service,
    )

    result = service.login(
        " TEST@EXAMPLE.COM ",
        "secret",
    )

    assert result.success is True
    assert result.user_id == 1
    assert result.email == "test@example.com"
    assert result.roles == ("Patient",)
    assert result.error is None

    assert (
        repository.requested_email
        == "test@example.com"
    )


def test_login_fails_for_unknown_user():
    repository = FakeAuthRepository(None)
    password_service = FakePasswordService()

    service = LoginService(
        auth_repository=repository,
        password_service=password_service,
    )

    result = service.login(
        "unknown@example.com",
        "secret",
    )

    assert result.success is False
    assert result.user_id is None
    assert result.error == (
        "Invalid email or password."
    )


def test_login_fails_for_wrong_password():
    user = make_user()

    repository = FakeAuthRepository(user)
    password_service = FakePasswordService(
        valid=False
    )

    service = LoginService(
        auth_repository=repository,
        password_service=password_service,
    )

    result = service.login(
        "test@example.com",
        "wrong-password",
    )

    assert result.success is False
    assert result.user_id is None
    assert result.error == (
        "Invalid email or password."
    )


def test_login_fails_for_inactive_account():
    user = make_user(
        status="Disabled"
    )

    repository = FakeAuthRepository(user)
    password_service = FakePasswordService(
        valid=True
    )

    service = LoginService(
        auth_repository=repository,
        password_service=password_service,
    )

    result = service.login(
        "test@example.com",
        "secret",
    )

    assert result.success is False
    assert result.user_id is None
    assert result.error == (
        "Account is not active."
    )


def test_login_returns_all_roles():
    user = make_user(
        roles=(
            "Patient",
            "Doctor",
        )
    )

    repository = FakeAuthRepository(user)
    password_service = FakePasswordService(
        valid=True
    )

    service = LoginService(
        auth_repository=repository,
        password_service=password_service,
    )

    result = service.login(
        "test@example.com",
        "secret",
    )

    assert result.success is True
    assert result.roles == (
        "Patient",
        "Doctor",
    )


def test_login_rejects_empty_email():
    repository = FakeAuthRepository()
    password_service = FakePasswordService()

    service = LoginService(
        auth_repository=repository,
        password_service=password_service,
    )

    result = service.login(
        "",
        "secret",
    )

    assert result.success is False
    assert result.error == (
        "Invalid email or password."
    )


def test_login_rejects_empty_password():
    repository = FakeAuthRepository()
    password_service = FakePasswordService()

    service = LoginService(
        auth_repository=repository,
        password_service=password_service,
    )

    result = service.login(
        "test@example.com",
        "",
    )

    assert result.success is False
    assert result.error == (
        "Invalid email or password."
    )