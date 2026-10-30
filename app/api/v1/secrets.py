from fastapi import APIRouter

from app.dependency import CurrentUserDep, OptionalUserDep, SessionDep
from app.schemas import (
    SecretChange,
    SecretCreate,
    SecretsAllTokensRead,
    SecretTokenRead,
)
from app.service import secrets as secret_service

router = APIRouter()

@router.get("/secrets/{secret_token}")
def consume_secret(secret_token: str, session: SessionDep):
    return secret_service.consume_secret(secret_token, session)

@router.post("/secrets", response_model=SecretTokenRead)
def create_secret(secret_request: SecretCreate, session: SessionDep, current_user: OptionalUserDep):
    return secret_service.create_secret(secret_request, session, current_user)

@router.get("/secrets", response_model=SecretsAllTokensRead)
def get_all_my_tokens(current_user: CurrentUserDep, session: SessionDep):
    return secret_service.get_all_my_tokens(current_user, session)

@router.put("/secrets/{secret_token}", response_model=SecretTokenRead)
def change_secret(secret_token: str, payload: SecretChange, current_user: CurrentUserDep, session: SessionDep):
    return secret_service.change_secret(secret_token, payload, current_user, session)

@router.delete("/secrets/{secret_token}")
def delete_secret(secret_token: str, current_user: CurrentUserDep, session: SessionDep):
    return secret_service.delete_secret(secret_token, current_user, session)
