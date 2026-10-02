from pydantic import BaseModel, Field


class CreateSecretRequest(BaseModel):
    secret: str = Field(min_length=1, max_length=2**12)
    time_to_live: int = Field(ge=1, le=86400)