from .models import (
    ConversationMsg,
    TriageResult,
    TriageSession,
)
from .session import SessionLocal


def test_triage_models() -> None:
    with SessionLocal() as session:

        # ---------------------------------------------------------
        # Test triage sessions
        # ---------------------------------------------------------
        sessions = session.query(TriageSession).all()

        for triage_session in sessions:

            print(
                f"Session: "
                f"{triage_session.session_id}"
            )

            print(
                f"  Patient ID: "
                f"{triage_session.patient_id}"
            )

            print(
                f"  Status: "
                f"{triage_session.status}"
            )

            # -----------------------------------------------------
            # Test conversation messages
            # -----------------------------------------------------
            for message in triage_session.messages:
                print(
                    f"  Message: "
                    f"[{message.sender_type}] "
                    f"{message.content}"
                )

            # -----------------------------------------------------
            # Test triage result
            # -----------------------------------------------------
            if triage_session.result is not None:

                result = triage_session.result

                print(
                    f"  Result: "
                    f"{result.risk_level} "
                    f"({result.confidence_score}%)"
                )

                print(
                    f"  Recommendation: "
                    f"{result.recommendation}"
                )

        # ---------------------------------------------------------
        # Direct table queries
        # ---------------------------------------------------------
        messages = session.query(
            ConversationMsg
        ).all()

        results = session.query(
            TriageResult
        ).all()

        print(
            f"\nTotal messages: "
            f"{len(messages)}"
        )

        print(
            f"Total results: "
            f"{len(results)}"
        )


if __name__ == "__main__":
    test_triage_models()