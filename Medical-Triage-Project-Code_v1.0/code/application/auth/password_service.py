import hashlib
import hmac
import secrets


class PasswordService:
    """
    Responsible for password hashing and verification.

    This service intentionally keeps password handling isolated
    from authentication and database logic.
    """

    _ALGORITHM = "sha256"
    _SALT_BYTES = 32
    _ITERATIONS = 310_000

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Hash a password using PBKDF2-HMAC-SHA256.

        Stored format:

            algorithm$iterations$salt$hash
        """

        if not isinstance(password, str):
            raise TypeError("Password must be a string.")

        if not password:
            raise ValueError("Password cannot be empty.")

        salt = secrets.token_bytes(cls._SALT_BYTES)

        password_hash = hashlib.pbkdf2_hmac(
            cls._ALGORITHM,
            password.encode("utf-8"),
            salt,
            cls._ITERATIONS,
        )

        return (
            f"{cls._ALGORITHM}$"
            f"{cls._ITERATIONS}$"
            f"{salt.hex()}$"
            f"{password_hash.hex()}"
        )

    @classmethod
    def verify_password(
        cls,
        password: str,
        stored_hash: str,
    ) -> bool:
        """
        Verify a plaintext password against a stored hash.
        """

        if not isinstance(password, str):
            return False

        if not isinstance(stored_hash, str):
            return False

        try:
            algorithm, iterations, salt_hex, hash_hex = (
                stored_hash.split("$")
            )

            if algorithm != cls._ALGORITHM:
                return False

            iterations = int(iterations)

            salt = bytes.fromhex(salt_hex)
            expected_hash = bytes.fromhex(hash_hex)

        except (
            ValueError,
            TypeError,
        ):
            return False

        actual_hash = hashlib.pbkdf2_hmac(
            algorithm,
            password.encode("utf-8"),
            salt,
            iterations,
        )

        return hmac.compare_digest(
            actual_hash,
            expected_hash,
        )