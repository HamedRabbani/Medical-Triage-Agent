from infrastructure.database.session import SessionLocal
from infrastructure.database.unit_of_work import UnitOfWork
from application.services.triage_service import TriageService
from application.services.triage_agent_service import TriageAgentService


def test_triage_agent_service() -> None:
    """Test Agent-to-Database persistence."""

    print("Starting TriageAgentService test...")

    with SessionLocal() as session:

        uow = UnitOfWork(session)

        triage_service = TriageService(uow)

        agent_service = TriageAgentService(
            triage_service
        )

        # Get an existing patient
        patients = uow.patients.get_all()

        print(f"Patients found: {len(patients)}")

        if not patients:
            print("No patient found. Test stopped.")
            return

        patient = patients[0]

        print(
            f"Using patient ID: "
            f"{patient.patient_id}"
        )

        # Simulate LangGraph output
        result = agent_service.save_triage_result(
            patient_id=patient.patient_id,
            content="I have chest pain.",
            risk_level="High",
            confidence_score=95.0,
            recommendation=(
                "Seek immediate medical attention."
            ),
        )

        print(
            f"Result ID: {result.result_id}"
        )

        print(
            f"Risk Level: {result.risk_level}"
        )

        print(
            f"Confidence: "
            f"{result.confidence_score}"
        )

        print(
            "TriageAgentService test passed."
        )


if __name__ == "__main__":
    test_triage_agent_service()