from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Secret(Base):
    __tablename__ = "secrets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    secret: Mapped[str]
    token: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime]
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
