from sqlalchemy.orm import sessionmaker

from .connection import engine


# Create a session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)