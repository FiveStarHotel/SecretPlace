from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.repository import auth as auth_repository
from app.security import validate_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_session() -> Generator[Session]:
    with SessionLocal() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credential_error_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Problems with credentials!",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        user_id = validate_access_token(token)
    except jwt.InvalidTokenError:
        raise credential_error_exception
    
    user = auth_repository.get_user_by_id(session, user_id)

    if not user:
        raise credential_error_exception
    
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]


