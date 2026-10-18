from fastapi import APIRouter

from app.dependency import CurrentUserDep, OptionalUserDep, SessionDep
from app.schemas import CreateSecretRequest
from app.service import secrets as secret_service

router = APIRouter()

@router.get("/secrets/{secret_token}")
def consume_secret(secret_token: str, session: SessionDep):
    return secret_service.consume_secret(secret_token, session)

@router.post("/secrets")
def create_secret(secret_request: CreateSecretRequest, session: SessionDep, current_user: OptionalUserDep):
    return secret_service.create_secret(secret_request, session, current_user)

@router.get("/secrets")
def get_all_my_tokens(current_user: CurrentUserDep, session: SessionDep):
    return secret_service.get_all_my_tokens(current_user, session)
