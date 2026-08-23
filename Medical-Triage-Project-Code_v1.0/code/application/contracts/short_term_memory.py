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

    missing_information: list[str] = Field(
        default_factory=list
    )

    current_question: str | None = None

    risk_context: dict = Field(
        default_factory=dict
    )

    intent: str | None = None