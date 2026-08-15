
from datetime import datetime, UTC
import uuid
from .models import (
    ConversationMsg,
    PatientProfile,
    TriageResult,
    TriageSession,
    UserAccount,
)
from .session import SessionLocal


# Test complete database ORM flow
def test_database_integration() -> None:
    with SessionLocal() as session:

        try:
            # Create test user
            user = UserAccount(
            email=f"test_{uuid.uuid4().hex}@example.com",
            password_hash="hamedrabbani123456789",
            phone=None,
            status="Active",
            created_at=datetime.now(UTC),
            
            )

            session.add(user)
            session.flush()

            # Create patient profile
            patient = PatientProfile(
                user_id=user.user_id,
                first_name="hamed",
                last_name="rabbani",
                date_of_birth=datetime(1995, 1, 1),
                gender="Unknown",
                national_id="hamed-rabbani-001",
                created_at=datetime.now(UTC),
            )

            session.add(patient)
            session.flush()

            # Create triage session
            triage_session = TriageSession(
                patient_id=patient.patient_id,
                start_time=datetime.now(UTC),
                status="Active",
            )

            session.add(triage_session)
            session.flush()

            # Create conversation message
            message = ConversationMsg(
                session_id=triage_session.session_id,
                sender_type="Patient",
                content="I have chest pain.",
                timestamp=datetime.now(UTC),
            )

            session.add(message)

            # Create triage result
            result = TriageResult(
                session_id=triage_session.session_id,
                risk_level="High",
                confidence_score=95.00,
                recommendation="Seek immediate medical attention.",
                created_at=datetime.now(UTC),
            )

            session.add(result)

            # Commit test transaction
            session.commit()

            # Verify relationships
            session.refresh(triage_session)

            print("\n=== Integration Test ===")
            print(f"User: {user.email}")
            print(
                f"Patient: "
                f"{patient.first_name} {patient.last_name}"
            )
            print(f"Session ID: {triage_session.session_id}")

            print("\nMessages:")
            for msg in triage_session.messages:
                print(f"  [{msg.sender_type}] {msg.content}")

            print("\nResults:")
            for triage_result in triage_session.results:
                print(
                    f"  Risk: {triage_result.risk_level}"
                    f" | Confidence: "
                    f"{triage_result.confidence_score}"
                )

            print("\nIntegration test passed.")

            # Remove test data
            session.delete(result)
            session.delete(message)
            session.delete(triage_session)
            session.delete(patient)
            session.delete(user)

            session.commit()

            print("Test data cleaned up.")

        except Exception:
            session.rollback()
            raise



if __name__ == "__main__":
    test_database_integration()