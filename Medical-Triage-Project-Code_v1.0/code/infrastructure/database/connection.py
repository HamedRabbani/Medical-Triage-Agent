import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


# Load environment variables
load_dotenv()


# SQL Server connection string
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured."
    )


# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)