from datetime import UTC, datetime
import uuid

from .models import (
    ConversationMsg,
    PatientProfile,
    TriageResult,
    TriageSession,
    UserAccount,
)
from .session import SessionLocal


def test_database_integration() -> None:
    with SessionLocal() as session:

        try:
            # ---------------------------------------------------------
            # Create test user
            # ---------------------------------------------------------
            user = UserAccount(
                email=f"test_{uuid.uuid4().hex}@example.com",
                password_hash="hamedrabbani123456789",
                phone=None,
                status="Active",
                created_at=datetime.now(UTC),
            )

            session.add(user)
            session.flush()

            # ---------------------------------------------------------
            # Create patient profile
            # ---------------------------------------------------------
            patient = PatientProfile(
                user_id=user.user_id,
                first_name="hamed",
                last_name="rabbani",
                date_of_birth=datetime(1995, 1, 1),
                gender="Male",
                national_id=f"T{uuid.uuid4().hex[:18]}",
                created_at=datetime.now(UTC),
            )

            session.add(patient)
            session.flush()

            # ---------------------------------------------------------
            # Create triage session
            # ---------------------------------------------------------
            triage_session = TriageSession(
                patient_id=patient.patient_id,
                start_time=datetime.now(UTC),
                status="Active",
            )

            session.add(triage_session)
            session.flush()

            # ---------------------------------------------------------
            # Create conversation message
            # ---------------------------------------------------------
            message = ConversationMsg(
                session_id=triage_session.session_id,
                sender_type="Patient",
                content="I have chest pain.",
                timestamp=datetime.now(UTC),
            )

            session.add(message)

            # ---------------------------------------------------------
            # Create triage result
            # ---------------------------------------------------------
            result = TriageResult(
                session_id=triage_session.session_id,
                risk_level="High",
                confidence_score=95.00,
                recommendation="Seek immediate medical attention.",
                created_at=datetime.now(UTC),
            )

            session.add(result)

            # ---------------------------------------------------------
            # Commit
            # ---------------------------------------------------------
            session.commit()

            # ---------------------------------------------------------
            # Verify relationships
            # ---------------------------------------------------------
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
                print(
                    f"  [{msg.sender_type}] "
                    f"{msg.content}"
                )

            print("\nResult:")

            if triage_session.result is not None:
                print(
                    f"  Risk: "
                    f"{triage_session.result.risk_level}"
                    f" | Confidence: "
                    f"{triage_session.result.confidence_score}"
                )

                print(
                    f"  Recommendation: "
                    f"{triage_session.result.recommendation}"
                )

            # ---------------------------------------------------------
            # Cleanup
            # ---------------------------------------------------------
            session.delete(result)
            session.delete(message)
            session.delete(triage_session)
            session.delete(patient)
            session.delete(user)

            session.commit()

            print("\nIntegration test passed.")
            print("Test data cleaned up.")

        except Exception:
            session.rollback()
            raise


if __name__ == "__main__":
    test_database_integration()