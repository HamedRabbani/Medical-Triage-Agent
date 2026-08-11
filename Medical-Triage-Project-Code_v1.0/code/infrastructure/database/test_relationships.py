from .models import UserAccount
from .session import SessionLocal


# Test ORM relationships
def test_user_relationships() -> None:
    with SessionLocal() as session:
        users = session.query(UserAccount).all()

        for user in users:
            print(f"User: {user.email}")

            for user_role in user.user_roles:
                print(f"  Role: {user_role.role.role_name}")


if __name__ == "__main__":
    test_user_relationships()