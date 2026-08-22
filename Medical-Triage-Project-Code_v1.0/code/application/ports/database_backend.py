from dataclasses import dataclass

from application.ports.conversation_history_port import (
    ConversationHistoryPort,
)
from application.ports.triage_persistence_port import (
    TriagePersistencePort,
)


@dataclass
class DatabaseBackend:
    """Persistence capabilities provided by one database backend."""

    triage: TriagePersistencePort
    conversation: ConversationHistoryPort

    def close(self) -> None:
        """Release backend resources when required."""
        return None