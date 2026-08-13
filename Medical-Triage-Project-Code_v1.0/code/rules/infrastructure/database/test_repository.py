from .repositories.user_repository import UserRepository
from .session import SessionLocal


def test_user_repository() -> None:
    with SessionLocal() as session:

        repository = UserRepository(session)

        users = repository.get_all()

        print(f"Total users: {len(users)}")

        if users:
            user = repository.get_by_id(users[0].user_id)

            print(f"User: {user.email}")

            found_user = repository.get_by_email(
                user.email
            )

            print(f"Found: {found_user.email}")


if __name__ == "__main__":
    test_user_repository()