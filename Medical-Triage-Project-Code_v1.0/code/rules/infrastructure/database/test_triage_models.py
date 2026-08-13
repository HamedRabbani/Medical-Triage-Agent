from .models import (
    ConversationMsg,
    TriageResult,
    TriageSession,
)
from .session import SessionLocal


# Test triage ORM relationships
def test_triage_models() -> None:
    with SessionLocal() as session:

        # Test triage sessions
        sessions = session.query(TriageSession).all()

        for triage_session in sessions:
            print(f"Session: {triage_session.session_id}")
            print(f"  Patient ID: {triage_session.patient_id}")
            print(f"  Status: {triage_session.status}")

            # Test conversation messages
            for message in triage_session.messages:
                print(
                    f"  Message: "
                    f"[{message.sender_type}] "
                    f"{message.content}"
                )

            # Test triage results
            for result in triage_session.results:
                print(
                    f"  Result: "
                    f"{result.risk_level} "
                    f"({result.confidence_score}%)"
                )
                print(
                    f"  Recommendation: "
                    f"{result.recommendation}"
                )

        # Direct table queries
        messages = session.query(ConversationMsg).all()
        results = session.query(TriageResult).all()

        print(f"\nTotal messages: {len(messages)}")
        print(f"Total results: {len(results)}")


if __name__ == "__main__":
    test_triage_models()