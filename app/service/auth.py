from sqlite3 import IntegrityError

from fastapi import HTTPException, status
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

    user = User(
        username=data.username,
        hashed_password=hash_password(data.password)
    )

    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Login '{data.username}' is already taken!"
        )
    
    session.refresh(user)
    return UserRead.model_validate(user)
