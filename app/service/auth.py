from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Login '{data.username}' is already taken!"
        )

    user = repository_auth.create_user(
        session,
        data.username,
        data.password
    )

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Login '{data.username}' is already taken!"
        )

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
    credentials_error_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password!",
        headers={"WWW-Authenticate": "Bearer"}
    )

    user = repository_auth.get_user_by_username(session, username)

    if user is None:
        verify_passowrd(password, DUMMY_HASH)
        raise credentials_error_exception
    
    if not verify_passowrd(password, user.hashed_password):
        raise credentials_error_exception
    
    return issue_token(user.id, session)
