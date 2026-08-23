from typing import Protocol

from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.memory_context import (
    MemoryContext,
)
from application.contracts.short_term_memory import (
    ShortTermMemory,
)


class MemoryPort(Protocol):
    """Application-level contract for memory management."""

    def load(
        self,
        session_id: int,
        history: list[dict],
    ) -> ShortTermMemory:
        ...

    def retrieve(
        self,
        patient_id: int,
        session_id: int,
        history: list[dict],
    ) -> MemoryContext:
        ...

    def update(
        self,
        memory: ShortTermMemory,
        extraction: ConversationExtraction,
    ) -> ShortTermMemory:
        ...