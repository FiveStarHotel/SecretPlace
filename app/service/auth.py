from datetime import UTC, datetime, timedelta

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.exceptions import (
    CredentialsError,
    InactiveUserError,
    InvalidRefreshTokenError,
    UsernameOccupiedError,
)
from app.repository import auth as repository_auth
from app.repository import refresh_tokens as repository_refresh_tokens
from app.schemas import Token, UserCreate, UserRead
from app.security import (
    DUMMY_HASH,
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
    verify_passowrd,
)


def register(data: UserCreate, session: Session):
    if repository_auth.get_user_by_username(session, data.username) is not None:
        raise UsernameOccupiedError()

    user = repository_auth.create_user(
        session,
        data.username,
        data.password
    )

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise UsernameOccupiedError()

    return UserRead.model_validate(user)


def issue_token(user_id: int, session: Session) -> Token:
    expires_at = datetime.now(UTC) + timedelta(seconds=settings.refresh_token_ttl)
    token = create_refresh_token()

    repository_refresh_tokens.create_refresh_token(
        session,
        user_id,
        hash_refresh_token(token),
        expires_at
    )

    session.commit()

    return Token(
        access_token=create_access_token(user_id),
        refresh_token=token
    )


def login(username: str, password: str, session: Session):
    user = repository_auth.get_user_by_username(session, username)

    if user is None:
        verify_passowrd(password, DUMMY_HASH)
        raise CredentialsError()
    
    if not verify_passowrd(password, user.hashed_password):
        raise CredentialsError()
    
    return issue_token(user.id, session)


def refresh_access_token(refresh_token: str, session: Session):
    stored_refresh_token = repository_refresh_tokens.get_refresh_token_by_hash(
        session=session,
        hashed_token=hash_refresh_token(refresh_token)
    )

    if stored_refresh_token is None:
        raise InvalidRefreshTokenError()
    
    user = repository_auth.get_user_by_id(session, stored_refresh_token.user_id)

    if user is None:
        raise InvalidRefreshTokenError()
    
    if stored_refresh_token.expires_at <= datetime.now(UTC):
        raise InvalidRefreshTokenError()

    if stored_refresh_token.revoked_at is not None:
        raise InvalidRefreshTokenError()

    if not user.is_active:
        raise InactiveUserError()

    repository_refresh_tokens.revoke_refresh_token(session, stored_refresh_token)

    return issue_token(user.id, session)


def logout(refresh_token: str, session: Session):
    stored_refresh_token = repository_refresh_tokens.get_refresh_token_by_hash(
        session=session,
        hashed_token=hash_refresh_token(refresh_token)
    )

    if stored_refresh_token is None or stored_refresh_token.revoked_at is not None:
        return

    repository_refresh_tokens.revoke_refresh_token(
        session=session,
        token=stored_refresh_token
    )

    session.commit()


def logout_all(refresh_token: str, session: Session):
    stored_refresh_token = repository_refresh_tokens.get_refresh_token_by_hash(
        session=session,
        hashed_token=hash_refresh_token(refresh_token)
    )

    if stored_refresh_token is None:
        raise InvalidRefreshTokenError()
    
    if stored_refresh_token.expires_at <= datetime.now(UTC):
        raise InvalidRefreshTokenError()
    
    if stored_refresh_token.revoked_at is not None:
        raise InvalidRefreshTokenError()
    
    repository_refresh_tokens.revoke_all_user_refresh_tokens(session, stored_refresh_token.user_id)

    session.commit()
