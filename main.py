from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

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

FRONTEND_DIST = Path(__file__).parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    # SPA: any non-API path (/, /login, /s/<token>) returns index.html, routing is done by React
    @app.get("/{path:path}", include_in_schema=False)
    def frontend(path: str):
        if path.startswith("api/"):
            raise HTTPException(status_code=404)
        return FileResponse(FRONTEND_DIST / "index.html")
