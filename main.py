from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.secrets import router as secrets_router
from app.api.v1.users import router as users_router
from app.exceptions import AppError

app = FastAPI()

@app.exception_handler(AppError)
async def exception_handler(request: Request, exc: AppError):
    return JSONResponse(
        content=exc.detail,
        status_code=exc.status_code
    )

app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(secrets_router, prefix="/api/v1", tags=["secrets management"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
