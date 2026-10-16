from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


def get_user_by_username(session: Session, username: str) -> User | None:
    stmt = (
        select(User)
        .where(User.username == username)
    )

    user = session.scalar(stmt)

    return user
