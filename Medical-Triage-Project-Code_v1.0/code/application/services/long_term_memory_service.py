from application.contracts.long_term_memory import (
    LongTermMemory,
)


class LongTermMemoryService:
    """
    Service responsible for retrieving persistent patient memory.

    Long-term memory includes:
    - Patient profile
    - Medical history
    - Previous triage results
    """

    def __init__(
        self,
        patient_repository,
        medical_record_repository,
        triage_repository,
    ):

        self.patient_repository = (
            patient_repository
        )

        self.medical_record_repository = (
            medical_record_repository
        )

        self.triage_repository = (
            triage_repository
        )


    def retrieve(
        self,
        patient_id: int,
    ) -> LongTermMemory:
        """
        Retrieve long-term memory for a patient.
        """

        # =====================================================
        # Patient Profile
        # =====================================================

        patient = None

        if self.patient_repository is not None:

            patient = (
                self.patient_repository
                .get_patient_by_id(
                    patient_id
                )
            )


        patient_profile = None

        if patient is not None:

            patient_profile = {
                "patient_id": (
                    patient.patient_id
                ),
                "user_id": (
                    patient.user_id
                ),
                "first_name": (
                    patient.first_name
                ),
                "last_name": (
                    patient.last_name
                ),
                "date_of_birth": (
                    patient.date_of_birth
                ),
                "gender": (
                    patient.gender
                ),
            }


        # =====================================================
        # Medical History
        # =====================================================

        medical_records = []

        if self.medical_record_repository is not None:

            medical_records = (
                self.medical_record_repository
                .get_by_patient_id(
                    patient_id
                )
                or []
            )


        medical_history = [

            {
                "record_id": (
                    record.record_id
                ),
                "patient_id": (
                    record.patient_id
                ),
                "condition": (
                    record.condition
                ),
                "description": (
                    record.description
                ),
                "record_type": (
                    record.record_type
                ),
                "created_at": (
                    record.created_at
                ),
            }

            for record in medical_records

        ]


        # =====================================================
        # Previous Triage Results
        # =====================================================

        triage_results = []

        if self.triage_repository is not None:

            triage_results = (
                self.triage_repository
                .get_results_by_patient_id(
                    patient_id
                )
                or []
            )


        previous_triage_results = [

            {
                "result_id": (
                    result.result_id
                ),
                "session_id": (
                    result.session_id
                ),
                "risk_level": (
                    result.risk_level
                ),
                "confidence_score": (
                    result.confidence_score
                ),
                "recommendation": (
                    result.recommendation
                ),
                "created_at": (
                    result.created_at
                ),
            }

            for result in triage_results

        ]


        # =====================================================
        # Return Memory Object
        # =====================================================

        return LongTermMemory(
            patient_profile=patient_profile,
            medical_history=medical_history,
            previous_triage_results=(
                previous_triage_results
            ),
        )