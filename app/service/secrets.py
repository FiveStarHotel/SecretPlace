from fastapi import Response, status
from sqlalchemy.orm import Session

from app.exceptions import SecretNotFoundError
from app.models import User
from app.repository import secrets as secrets_repository
from app.schemas import (
    SecretChange,
    SecretCreate,
    SecretRead,
    SecretsAllTokensRead,
    SecretTokenRead,
)


def consume_secret(secret_token: str, session: Session):
    secret = secrets_repository.consume_secret(
        session,
        secret_token
    )

    # Это не только случай "ненахода"
    # Секрет также мог существовать, но при этом просрочиться + не собранным сборщиком старости
    # Он бы и так удалился + вернулся бы None
    if secret is None:
        session.commit()
        raise SecretNotFoundError()

    session.commit()

    return SecretRead.model_validate(secret)


def create_secret(secret_request: SecretCreate, session: Session, current_user: User | None):
    new_secret = secrets_repository.create_secret(
        session=session,
        secret_content=secret_request.secret,
        time_to_live=secret_request.time_to_live,
        user_id=current_user.id if current_user is not None else None
    )

    session.commit()

    return SecretTokenRead.model_validate(new_secret)


def get_all_my_tokens(current_user: User, session: Session):
    tokens_list = secrets_repository.get_all_users_tokens(
        session,
        current_user.id
    )

    return SecretsAllTokensRead(
        tokens=tokens_list
    )


def change_secret(secret_token: str, payload: SecretChange, current_user: User, session: Session):
    changed_secret = secrets_repository.change_secret(
        session,
        secret_token,
        current_user.id,
        payload.secret
    )

    if changed_secret is None:
        raise SecretNotFoundError()

    session.commit()

    return SecretTokenRead.model_validate(change_secret)


def delete_secret(secret_token: str, current_user: User, session: Session):
    delete_status = secrets_repository.delete_secret(session, secret_token, current_user.id)

    if not delete_status:
        raise SecretNotFoundError()

    session.commit()
    
    return Response(status_code=status.HTTP_200_OK)
