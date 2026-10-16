from fastapi import APIRouter

from app.dependence import SessionDep
from app.schemas import CreateSecretRequest
from app.service import secrets as secret_service

router = APIRouter()

@router.get("/secrets/{secret_token}")
def consume_secret(secret_token: str, session: SessionDep):
    return secret_service.consume_secret(secret_token, session)

@router.post("/secrets/")
def create_secret(secret_request: CreateSecretRequest, session: SessionDep):
    return secret_service.create_secret(secret_request, session)