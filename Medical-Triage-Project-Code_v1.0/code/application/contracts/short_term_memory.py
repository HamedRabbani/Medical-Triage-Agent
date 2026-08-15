from pydantic import BaseModel, Field

from application.contracts.conversation_extraction import (
    ConversationExtraction,
)


class ShortTermMemory(BaseModel):
    session_id: int

    recent_messages: list[dict] = Field(
        default_factory=list
    )

    medical_context: ConversationExtraction = Field(
        default_factory=ConversationExtraction
    )

    intent: str | None = None