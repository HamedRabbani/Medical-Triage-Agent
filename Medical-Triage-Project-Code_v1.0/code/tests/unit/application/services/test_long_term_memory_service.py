from datetime import date, datetime

from application.services.long_term_memory_service import (
    LongTermMemoryService,
)


class FakePatient:

    patient_id = 1
    user_id = 10
    first_name = "Hamed"
    last_name = "Test"
    gender = "Male"
    date_of_birth = date(1997, 1, 1)


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

    def get_patient_by_id(
        self,
        patient_id,
    ):
        return FakePatient()


class FakeMedicalRecordRepository:

    def get_by_patient_id(
        self,
        patient_id,
    ):
        return [
            FakeRecord()
        ]


class FakeTriageRepository:

    def get_results_by_patient_id(
        self,
        patient_id,
    ):
        return [
            FakeTriageResult()
        ]


def test_retrieve_long_term_memory():

    service = LongTermMemoryService(
        patient_repository=FakePatientRepository(),
        medical_record_repository=(
            FakeMedicalRecordRepository()
        ),
        triage_repository=FakeTriageRepository(),
    )

    memory = service.retrieve(
        patient_id=1
    )

    # Patient profile

    assert (
        memory.patient_profile["patient_id"]
        == 1
    )

    assert (
        memory.patient_profile["user_id"]
        == 10
    )

    assert (
        memory.patient_profile["first_name"]
        == "Hamed"
    )


    # Medical history

    assert len(
        memory.medical_history
    ) == 1

    assert (
        memory.medical_history[0]["condition"]
        == "Headache"
    )


    # Previous triage

    assert len(
        memory.previous_triage_results
    ) == 1

    assert (
        memory.previous_triage_results[0]["risk_level"]
        == "Low"
    )