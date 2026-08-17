from typing import Literal

from pydantic import BaseModel, Field


class ConversationIntent(BaseModel):
    intent: Literal[
        "TRIAGE",
        "GENERAL",
        "PROFILE",
    ]

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )