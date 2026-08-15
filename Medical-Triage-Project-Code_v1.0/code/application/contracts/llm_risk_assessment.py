from pydantic import BaseModel, Field


class LLMRiskAssessment(BaseModel):
    risk_level: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    red_flags: list[str]
    recommendation: str