from fastapi import APIRouter

from app.schemas import CreateSecretRequest
from app.service import secrets as secret_service

router = APIRouter()

@router.get("/secrets/{secret_token}")
def consume_secret(secret_token: str):
    return secret_service.consume_secret(secret_token)

@router.post("/secrets/")
def create_secret(secret_request: CreateSecretRequest):
    return secret_service.create_secret(secret_request)