from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, StringConstraints

SECRET_LENGTH_MIN = 1
SECRET_LENGTH_MAX = 2**12

SECRET_TTL_SEC_MIN = 60
SECRET_TTL_SEC_MAX = 24 * 60 * 60

USERNAME_MIN_LENGTH = 3
USERNMAE_MAX_LENGTH = 32

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128

def _not_blank(value: str) -> str:
    if not value.strip():
        raise ValueError("Can't be blank!")
    return value


class SecretCreate(BaseModel):
    secret: str = Field(min_length=SECRET_LENGTH_MIN, max_length=SECRET_LENGTH_MAX)
    time_to_live: int = Field(ge=SECRET_TTL_SEC_MIN, le=SECRET_TTL_SEC_MAX)


class SecretRead(BaseModel):
    model_config = {"from_attributes": True}

    secret: str


class SecretTokenRead(BaseModel):
    model_config = {"from_attributes": True}

    token: str


class SecretsAllTokensRead(BaseModel):
    tokens: list[str]


class SecretChange(BaseModel):
    secret: str = Field(min_length=SECRET_LENGTH_MIN, max_length=SECRET_LENGTH_MAX)


Username = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=USERNAME_MIN_LENGTH, max_length=USERNMAE_MAX_LENGTH)
]
Password = Annotated[
    str,
    StringConstraints(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH),
    AfterValidator(_not_blank)
]


class UserCreate(BaseModel):
    username: Username
    password: Password


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str
