from pydantic import BaseModel, Field


class GeneralConversationResponse(BaseModel):
    response: str = Field(
        min_length=1,
    )