from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.repository import secrets as secrets_repository
from app.schemas import CreateSecretRequest
from app.service.auth import repository_auth


def consume_secret(secret_token: str, session: Session):
    secret = secrets_repository.consume_secret(
        session,
        secret_token
    )

    if secret is None:
        session.commit()
        raise HTTPException(
            status_code=404,
            detail=f"Secret with token '{secret_token}' doesn't exist!"
        )

    secret_content = secret.secret

    session.commit()

    return {
        "content": secret_content
    }

def create_secret(secret_request: CreateSecretRequest, session: Session, current_user: User | None):
    new_secret = secrets_repository.create_secret(
        session=session,
        secret_content=secret_request.secret,
        time_to_live=secret_request.time_to_live,
        user_id=current_user.id if current_user is not None else None
    )

    session.commit()

    return {
        "token": new_secret.token
    }


def delete_expired_secrets():
    with SessionLocal() as session:
        secrets_repository.delete_expired_secrets(session)
        session.commit()


def get_all_my_tokens(current_user: User, session: Session):
    tokens_list = secrets_repository.get_all_users_tokens(
        session,
        current_user.id
    )

    return {
        "tokens": tokens_list
    }
