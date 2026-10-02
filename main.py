from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.secrets import router as secrets_router
from app.database import Base, engine

app = FastAPI()

app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(secrets_router, prefix="/api/v1", tags=["secrets management"])

Base.metadata.create_all(bind=engine)