from typing import Protocol

from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.short_term_memory import (
    ShortTermMemory,
)


class MemoryPort(Protocol):
    """Application-level contract for short-term memory."""

    def load(
        self,
        session_id: int,
        history: list[dict],
    ) -> ShortTermMemory:
        ...

    def update(
        self,
        memory: ShortTermMemory,
        extraction: ConversationExtraction,
    ) -> ShortTermMemory:
        ...