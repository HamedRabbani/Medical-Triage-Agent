import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

DB_BACKEND = (
    os.getenv(
        "DB_BACKEND",
        "sqlserver",
    )
    .strip()
    .lower()
)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured."
    )


SUPPORTED_BACKENDS = {
    "sqlserver",
    "supabase",
}

if DB_BACKEND not in SUPPORTED_BACKENDS:
    raise RuntimeError(
        f"Unsupported DB_BACKEND: {DB_BACKEND}. "
        f"Supported values: "
        f"{', '.join(sorted(SUPPORTED_BACKENDS))}"
    )


engine = create_engine(
    DATABASE_URL,
    echo=False,
)