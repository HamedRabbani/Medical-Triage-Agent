from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# SQL Server connection configuration
DATABASE_URL = URL.create(
    "mssql+pyodbc",
    host="localhost",
    database="MedicalTriageDB",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "trusted_connection": "yes",
        "TrustServerCertificate": "yes",
    },
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)