import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )
else:
    engine = None