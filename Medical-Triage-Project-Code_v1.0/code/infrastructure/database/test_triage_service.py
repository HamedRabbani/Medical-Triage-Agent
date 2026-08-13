from infrastructure.database.session import SessionLocal
from infrastructure.database.unit_of_work import UnitOfWork
from application.services.triage_service import TriageService


def test_triage_service() -> None:
    """Test the atomic triage workflow."""

    print("Starting triage service test...")

    with SessionLocal() as session:

        uow = UnitOfWork(session)
        service = TriageService(uow)

        patients = uow.patients.get_all()

        print(f"Patients found: {len(patients)}")

        if not patients:
            print("No patient found. Test stopped.")
            return

        patient = patients[0]

        print(f"Using patient ID: {patient.patient_id}")

        result = service.process_triage(
            patient_id=patient.patient_id,
            content="I have chest pain.",
            risk_level="High",
            confidence_score=95.0,
            recommendation="Seek immediate medical attention.",
        )

        print(f"Result ID: {result.result_id}")
        print(f"Risk Level: {result.risk_level}")
        print(f"Confidence: {result.confidence_score}")

        print("Atomic triage process succeeded.")


if __name__ == "__main__":
    test_triage_service()