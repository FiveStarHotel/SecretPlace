from datetime import timedelta

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import Secret
from app.utils import generate_token, utc_now


def create_secret(session: Session, secret_content: str, time_to_live: int):
    expires_at = utc_now() + timedelta(seconds=time_to_live)

    new_secret = Secret(
        secret=secret_content,
        token=generate_token(),
        expires_at=expires_at
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