from .models.user_account import UserAccount
from .session import SessionLocal


# Test ORM SELECT operation
def test_user_account() -> None:
    with SessionLocal() as session:
        users = session.query(UserAccount).all()

        for user in users:
            print(
                user.user_id,
                user.email,
                user.status,
                
            )


if __name__ == "__main__":
    test_user_account()