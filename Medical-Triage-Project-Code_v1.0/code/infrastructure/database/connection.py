import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL


DATABASE_URL = URL.create(
    "mssql+pyodbc",
    username="medical_app",
    password="Hamed/.@#123",
    host="localhost",
    database="MedicalTriageDB",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes",
    },
)


engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)