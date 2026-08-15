from infrastructure.database.models.user_account import UserAccount
from infrastructure.database.session import SessionLocal
from infrastructure.database.unit_of_work import UnitOfWork
from datetime import datetime,UTC

def test_unit_of_work_rollback() -> None:
    test_email = "rollback_test@example.com"

    with SessionLocal() as session:

        try:
            with UnitOfWork(session) as uow:

                user = UserAccount(
                email=test_email,
                password_hash="rollback_test_hash",
                phone=None,
                status="Active",
                created_at=datetime.now(UTC),
                )

                uow.users.add(user)

                print(f"Created test user: {test_email}")

                raise RuntimeError(
                    "Intentional error for rollback test"
                )

        except RuntimeError as exc:
            print(f"Expected error: {exc}")

        repository = UnitOfWork(session).users

        user_after_rollback = repository.get_by_email(
            test_email
        )

        if user_after_rollback is None:
            print("Rollback successful.")
        else:
            raise AssertionError(
                "Rollback failed: test user still exists."
            )


if __name__ == "__main__":
    test_unit_of_work_rollback()