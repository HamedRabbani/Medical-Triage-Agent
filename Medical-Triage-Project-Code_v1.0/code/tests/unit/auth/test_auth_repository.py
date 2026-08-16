from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from infrastructure.auth.auth_repository import AuthRepository
from infrastructure.database.models.role import Role
from infrastructure.database.models.user_account import UserAccount
from infrastructure.database.models.user_role import UserRole


def create_test_database():
    """
    Create the complete authentication schema required
    by AuthRepository tests.
    """

    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
    )

    Role.__table__.create(engine)
    UserAccount.__table__.create(engine)
    UserRole.__table__.create(engine)

    return engine


def test_get_user_by_email():
    engine = create_test_database()

    with Session(engine) as session:

        role = Role(
            role_name="Patient",
        )

        user = UserAccount(
            email="test@example.com",
            password_hash="HASH",
            phone=None,
            status="Active",
        )

        session.add(role)
        session.add(user)
        session.flush()

        user_role = UserRole(
            user_id=user.user_id,
            role_id=role.role_id,
        )

        session.add(user_role)
        session.commit()

        repository = AuthRepository(session)

        result = repository.get_user_by_email(
            "test@example.com"
        )

        assert result is not None
        assert result.email == "test@example.com"
        assert result.password_hash == "HASH"

        assert len(result.user_roles) == 1
        assert result.user_roles[0].role.role_name == "Patient"


def test_get_user_by_email_returns_none_for_unknown_user():
    engine = create_test_database()

    with Session(engine) as session:

        repository = AuthRepository(session)

        result = repository.get_user_by_email(
            "unknown@example.com"
        )

        assert result is None