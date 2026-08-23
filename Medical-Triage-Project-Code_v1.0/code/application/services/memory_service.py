from application.contracts.conversation_extraction import (
    ConversationExtraction,
)

from application.contracts.memory_context import (
    MemoryContext,
)

from application.contracts.short_term_memory import (
    ShortTermMemory,
)

from application.ports.memory_port import (
    MemoryPort,
)

from application.services.short_term_memory_service import (
    ShortTermMemoryService,
)


class MemoryService(MemoryPort):
    """Application service for aggregated memory management."""

    def __init__(
        self,
        patient_repository,
        medical_record_repository,
        triage_repository,
    ):
        self.patient_repository = patient_repository

        self.medical_record_repository = (
            medical_record_repository
        )

        self.triage_repository = triage_repository

        self.short_term_memory_service = (
            ShortTermMemoryService()
        )

    def load(
        self,
        session_id: int,
        history: list[dict],
    ) -> ShortTermMemory:

        return self.short_term_memory_service.load(
            session_id=session_id,
            history=history,
        )

    def update(
        self,
        memory: ShortTermMemory,
        extraction: ConversationExtraction,
    ) -> ShortTermMemory:

        return self.short_term_memory_service.update(
            memory=memory,
            extraction=extraction,
        )

    def retrieve(
        self,
        patient_id: int,
        session_id: int,
        history: list[dict],
    ) -> MemoryContext:

        short_term = self.load(
            session_id=session_id,
            history=history,
        )

        patient = None

        if self.patient_repository is not None:
            patient = (
                self.patient_repository
                .get_patient_by_id(
                    patient_id
                )
            )

        medical_records = []

        if self.medical_record_repository is not None:
            medical_records = (
                self.medical_record_repository
                .get_by_patient_id(
                    patient_id
                )
            )

        triage_results = []

        if self.triage_repository is not None:
            triage_results = (
                self.triage_repository
                .get_results_by_patient_id(
                    patient_id
                )
            )

        patient_profile = None

        if patient is not None:

            patient_profile = {
                "patient_id": patient.patient_id,
                "user_id": patient.user_id,
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "date_of_birth": patient.date_of_birth,
                "gender": patient.gender,
            }

        medical_history = [
            {
                "record_id": record.record_id,
                "patient_id": record.patient_id,
                "condition": record.condition,
                "description": record.description,
                "record_type": record.record_type,
                "created_at": record.created_at,
            }
            for record in medical_records
        ]

        previous_triage_results = [
            {
                "result_id": result.result_id,
                "session_id": result.session_id,
                "risk_level": result.risk_level,
                "confidence_score": result.confidence_score,
                "recommendation": result.recommendation,
                "created_at": result.created_at,
            }
            for result in triage_results
        ]

        return MemoryContext(
            short_term=short_term,
            patient_profile=patient_profile,
            medical_history=medical_history,
            previous_triage_results=previous_triage_results,
        )