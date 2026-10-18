from datetime import timedelta

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from app.models import Secret
from app.utils import generate_token, utc_now


def create_secret(session: Session, secret_content: str, time_to_live: int, user_id: int | None):
    expires_at = utc_now() + timedelta(seconds=time_to_live)

    new_secret = Secret(
        secret=secret_content,
        token=generate_token(),
        expires_at=expires_at,
        user_id=user_id
    )
    
    session.add(new_secret)
    session.flush()

    return new_secret
    

def consume_secret(session: Session, token: str):
    stmt = (
        select(Secret)
        .where(Secret.token == token)
        .limit(1)
    )

    secret = session.scalar(stmt)
    delete_secret(session, token)

    

    if secret is None or secret.expires_at <= utc_now():
        return None

    return secret


def delete_secret(session: Session, token: str):
    stmt = (
        delete(Secret)
        .where(Secret.token == token)
    )

    session.execute(stmt)


def delete_expired_secrets(session: Session):
    stmt = delete(Secret).where(Secret.expires_at <= utc_now())
    session.execute(stmt)


def get_all_users_tokens(session: Session, user_id: int):
    stmt = (
        select(Secret.token)
        .where(Secret.user_id == user_id)
    )

    tokens = session.scalars(stmt).all()

    return list(tokens)


def change_secret(session: Session, token: str, user_id: int, new_content: str) -> Secret | None:
    stmt = (
        select(Secret)
        .where(and_(Secret.token == token, Secret.user_id == user_id))
        .limit(1)
    )

    secret = session.scalar(stmt)
    
    if secret is None:
        return None
    
    secret.secret = new_content

    session.flush()
    
    return secret
