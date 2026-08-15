from pydantic import BaseModel, Field


class ConversationExtraction(BaseModel):
    symptoms: list[str] = Field(
        default_factory=list
    )

    severity: str | None = None

    age: int | None = None

    duration: str | None = None

    red_flags: list[str] = Field(
        default_factory=list
    )