from pydantic import BaseModel


class LLMTestResponse(BaseModel):
    answer: str
    confidence: float