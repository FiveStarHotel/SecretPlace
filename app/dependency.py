from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_session() -> Generator[Session]:
    with SessionLocal() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
