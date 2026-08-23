from pydantic import BaseModel, Field

from application.contracts.short_term_memory import (
    ShortTermMemory,
)


class MemoryContext(BaseModel):
    """Aggregated memory context available to the application."""

    short_term: ShortTermMemory

    patient_profile: dict | None = None

    medical_history: list[dict] = Field(
        default_factory=list
    )

    previous_triage_results: list[dict] = Field(
        default_factory=list
    )