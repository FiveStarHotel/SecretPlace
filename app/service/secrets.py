from fastapi import HTTPException

from app.database import SessionLocal
from app.repository import secrets as secrets_repository
from app.schemas import CreateSecretRequest


def consume_secret(secret_token: str):
    with SessionLocal() as session:
        secret = secrets_repository.consume_secret(
            session,
            secret_token
        )

        if secret is None:
            raise HTTPException(
                status_code=404,
                detail=f"Secret with token '{secret_token}' doesn't exist!"
            )

        secret_content = secret.secret

        session.commit()

        return {
            "content": secret_content
        }

def create_secret(secret_request: CreateSecretRequest):
    with SessionLocal() as session:
        new_secret = secrets_repository.create_secret(
            session=session,
            secret_content=secret_request.secret,
            time_to_live=secret_request.time_to_live
        )

        session.commit()

        return {
            "token": new_secret.token
        }