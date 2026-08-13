from infrastructure.database.session import SessionLocal
from infrastructure.database.unit_of_work import UnitOfWork
from application.services.triage_service import TriageService


def test_triage_rollback() -> None:
    """Verify that failed triage is fully rolled back."""

    print("Starting rollback test...")

    with SessionLocal() as session:

        uow = UnitOfWork(session)
        service = TriageService(uow)

        patients = uow.patients.get_all()

        if not patients:
            print("No patient found.")
            return

        patient = patients[0]

        try:
            # Start normal workflow
            triage_session = service.start_session(
                patient.patient_id
            )

            uow.session.flush()

            print(
                f"Session created: "
                f"{triage_session.session_id}"
            )

            # Add message
            service.add_message(
                session_id=triage_session.session_id,
                sender_type="Patient",
                content="Rollback test message.",
            )

            print("Message created.")

            # Force an error
            raise RuntimeError(
                "Intentional failure for rollback test."
            )

        except RuntimeError as error:

            print(f"Expected error: {error}")

            uow.rollback()

            print("Rollback executed.")

        # Verify session does not exist
        remaining_session = (
            uow.triage.get_by_id(
                triage_session.session_id
            )
        )

        if remaining_session is None:
            print(
                "PASS: Triage session was rolled back."
            )
        else:
            print(
                "FAIL: Triage session still exists."
            )


if __name__ == "__main__":
    test_triage_rollback()