from pydantic import BaseModel, Field


class GeneralChatResponse(BaseModel):
    response: str = Field(
        ...,
        min_length=1,
    )