from pydantic import BaseModel


class LLMTestResponse(BaseModel):
    symptoms: list[str]