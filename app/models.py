from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Secret(Base):
    __tablename__ = "secrets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    secret: Mapped[str]
    token: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime]