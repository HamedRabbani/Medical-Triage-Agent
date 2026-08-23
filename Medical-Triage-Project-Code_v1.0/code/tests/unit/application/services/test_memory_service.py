from datetime import date, datetime

from application.services.memory_service import MemoryService


class FakeShortTermMemoryService:
    def load(self, session_id, history):
        return {
            "session_id": session_id,
            "recent_messages": history,
        }


class FakePatient:
    patient_id = 1
    user_id = 10
    first_name = "Hamed"
    last_name = "Test"
    date_of_birth = date(1997, 1, 1)
    gender = "Male"


class FakeRecord:
    record_id = 100
    patient_id = 1
    condition = "Headache"
    description = "Mild headache"
    record_type = "Clinical"
    created_at = datetime.now()


class FakeTriageResult:
    result_id = 200
    session_id = 50
    risk_level = "Low"
    confidence_score = 0.95
    recommendation = "Monitor symptoms"
    created_at = datetime.now()


class FakePatientRepository:
    def get_by_id(self, patient_id):
        return FakePatient()


class FakeMedicalRecordRepository:
    def get_by_patient_id(self, patient_id):
        return [FakeRecord()]


class FakeTriageRepository:
    def get_results_by_patient_id(self, patient_id):
        return [FakeTriageResult()]


def test_retrieve_memory_context():

    service = MemoryService(
        patient_repository=FakePatientRepository(),
        medical_record_repository=FakeMedicalRecordRepository(),
        triage_repository=FakeTriageRepository(),
    )

    service.short_term_memory_service = (
        FakeShortTermMemoryService()
    )

    context = service.retrieve(
        patient_id=1,
        session_id=50,
        history=[
            {
                "role": "user",
                "content": "I have a headache",
            }
        ],
    )

    assert context.short_term.session_id == 50

    assert context.patient_profile["patient_id"] == 1
    assert context.patient_profile["user_id"] == 10

    assert len(context.medical_history) == 1
    assert context.medical_history[0]["condition"] == "Headache"

    assert len(context.previous_triage_results) == 1
    assert (
        context.previous_triage_results[0]["risk_level"]
        == "Low"
    )