from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import RefreshToken


def create_refresh_token(
    session: Session,
    user_id: int,
    token_hash: str,
    expires_at: datetime
) -> RefreshToken:
    refresh_token = RefreshToken(
        token_hash=token_hash,
        user_id=user_id,
        created_at=datetime.now(UTC),
        expires_at=expires_at
    )

    session.add(refresh_token)
    session.flush()

    return refresh_token


def get_refresh_token_by_hash(session: Session, hashed_token: str) -> RefreshToken | None:
    stmt = (
        select(RefreshToken)
        .where(RefreshToken.token_hash == hashed_token)
        .limit(1)
    )

    token = session.scalar(stmt)

    return token


def revoke_refresh_token(session: Session, token: RefreshToken) -> None:
    token.revoked_at = datetime.now(UTC)
    session.flush()
