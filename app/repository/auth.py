from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.security import hash_password


def get_user_by_username(session: Session, username: str) -> User | None:
    stmt = (
        select(User)
        .where(User.username == username)
    )

    user = session.scalar(stmt)

    return user


def create_user(session: Session, username: str, password: str) -> User:
    user = User(
        username=username,
        hashed_password=hash_password(password)
    )

    session.add(user)
    session.flush()
    session.refresh(user)

    return user
