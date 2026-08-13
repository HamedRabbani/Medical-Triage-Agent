from .repositories.triage_repository import TriageRepository
from .session import SessionLocal


def test_triage_repository() -> None:
    with SessionLocal() as session:

        repository = TriageRepository(session)

        sessions = repository.get_all()

        print(f"Total sessions: {len(sessions)}")

        if sessions:
            triage_session = sessions[0]

            print(f"Session ID: {triage_session.session_id}")
            print(f"Patient ID: {triage_session.patient_id}")

            patient_sessions = repository.get_by_patient_id(
                triage_session.patient_id
            )

            print(
                f"Patient sessions: "
                f"{len(patient_sessions)}"
            )

            messages = repository.get_messages(
                triage_session.session_id
            )

            print(f"Messages: {len(messages)}")

            results = repository.get_results(
                triage_session.session_id
            )

            print(f"Results: {len(results)}")


if __name__ == "__main__":
    test_triage_repository()