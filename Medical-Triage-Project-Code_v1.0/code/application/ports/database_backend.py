from dataclasses import dataclass

from application.ports.auth_port import AuthPort
from application.ports.conversation_history_port import (
    ConversationHistoryPort,
)
from application.ports.patient_port import PatientPort
from application.ports.triage_persistence_port import (
    TriagePersistencePort,
)


@dataclass
class DatabaseBackend:
    triage: TriagePersistencePort
    conversation: ConversationHistoryPort
    patient: PatientPort
    auth: AuthPort | None = None

    def close(self) -> None:
        return None