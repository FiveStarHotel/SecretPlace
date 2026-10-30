from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.secrets import router as secrets_router
from app.api.v1.users import router as users_router

app = FastAPI()

app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(secrets_router, prefix="/api/v1", tags=["secrets management"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
