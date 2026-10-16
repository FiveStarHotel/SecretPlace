from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import User
from app.repository import auth as repository_auth
from app.schemas import UserCreate, UserRead
from app.security import hash_password


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
