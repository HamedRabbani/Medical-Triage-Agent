from typing import Literal

from pydantic import BaseModel, Field


class LLMRiskAssessment(BaseModel):

    risk_level: Literal["LOW", "HIGH"]

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    red_flags: list[str] = Field(
        default_factory=list,
    )

    recommendation: str