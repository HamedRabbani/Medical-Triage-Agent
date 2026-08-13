from .models import AuditLog, MedicalRecord, VerificationStatus
from .session import SessionLocal


# Test medical database models
def test_medical_models() -> None:
    with SessionLocal() as session:

        # Test verification statuses
        statuses = session.query(VerificationStatus).all()

        for status in statuses:
            print(
                f"Verification Status: "
                f"{status.status_id} - {status.status_name}"
            )

        # Test medical records
        records = session.query(MedicalRecord).all()

        for record in records:
            print(f"Medical Record: {record.record_id}")
            print(f"  Condition: {record.condition}")
            print(f"  Patient ID: {record.patient_id}")
            print(
                f"  Verification: "
                f"{record.verification_status.status_name}"
            )

        # Test audit logs
        logs = session.query(AuditLog).all()

        for log in logs:
            print(
                f"Audit: {log.action} "
                f"by User {log.user_id}"
            )


if __name__ == "__main__":
    test_medical_models()