from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, StringConstraints


def _not_blank(value: str) -> str:
    if not value.strip():
        raise ValueError("Can't be blank!")
    return value


class CreateSecretRequest(BaseModel):
    secret: str = Field(min_length=1, max_length=2**12)
    time_to_live: int = Field(ge=1, le=86400)


Username = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=3, max_length=32)
]
Password = Annotated[
    str,
    StringConstraints(min_length=8, max_length=128),
    AfterValidator(_not_blank)
]


class UserCreate(BaseModel):
    username: Username
    password: Password


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
