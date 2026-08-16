from application.auth.password_service import (
    PasswordService,
)


def test_password_hash_is_not_plaintext():
    password = "StrongPassword123!"

    hashed = PasswordService.hash_password(password)

    assert hashed != password


def test_password_hash_is_different_each_time():
    password = "StrongPassword123!"

    hash_1 = PasswordService.hash_password(password)
    hash_2 = PasswordService.hash_password(password)

    assert hash_1 != hash_2


def test_correct_password_is_verified():
    password = "StrongPassword123!"

    hashed = PasswordService.hash_password(password)

    assert PasswordService.verify_password(
        password,
        hashed,
    ) is True


def test_wrong_password_is_rejected():
    password = "StrongPassword123!"

    hashed = PasswordService.hash_password(password)

    assert PasswordService.verify_password(
        "WrongPassword123!",
        hashed,
    ) is False


def test_invalid_hash_is_rejected():
    assert PasswordService.verify_password(
        "password",
        "invalid-hash",
    ) is False


def test_empty_password_is_rejected():
    try:
        PasswordService.hash_password("")
    except ValueError:
        assert True
    else:
        assert False