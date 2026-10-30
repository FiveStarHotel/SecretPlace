import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.secrets import router as secrets_router
from app.api.v1.users import router as users_router
from app.service import secrets as secrets_service

CLEANUP_LOOP = 60

async def cleanup_loop():
    while True:
        try:
            await asyncio.to_thread(secrets_service.delete_expired_secrets)
        except Exception as error:
            print(f"Error while deleting old secrets: {error}", flush=True)

        await asyncio.sleep(CLEANUP_LOOP)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(cleanup_loop())
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan)

app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(secrets_router, prefix="/api/v1", tags=["secrets management"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
