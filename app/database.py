from datetime import UTC, datetime
from typing import Any, ClassVar, Self

from sqlalchemy import DateTime, TypeDecorator, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False
)

class UTCDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self: Self, value: datetime, dialect):
        if value is not None:
            if value.tzinfo is None:
                raise ValueError("Using naive datetime is prohibited! Use aware datetime!")
            value = value.astimezone(UTC).replace(tzinfo=None)
        return value
    
    def process_result_value(self: Self, value: datetime, dialect):
        if value is not None:
            value = value.replace(tzinfo=UTC)
        return value



class Base(DeclarativeBase):
    type_annotation_map: ClassVar[dict[Any, Any]] = {
        datetime: UTCDateTime
    }
