from .connection import engine


# Test database connection
def test_connection() -> None:
    try:
        with engine.connect():
            print("Database connection successful.")

    except Exception as exc:
        print("Database connection failed.")
        print(exc)


if __name__ == "__main__":
    test_connection()