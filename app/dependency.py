from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.exceptions import InvalidAccessTokenError
from app.models import User
from app.repository import auth as auth_repository
from app.security import validate_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_session() -> Generator[Session]:
    with SessionLocal() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    try:
        user_id = validate_access_token(token)
    except jwt.InvalidTokenError:
        raise InvalidAccessTokenError()
    
    user = auth_repository.get_user_by_id(session, user_id)

    if not user:
        raise InvalidAccessTokenError()
    
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_optional_user(token: Annotated[str | None, Depends(oauth2_scheme_optional)], session: SessionDep) -> User | None:
    if token is None:
        return None

    return get_current_user(token, session)

OptionalUserDep = Annotated[User | None, Depends(get_optional_user)]
