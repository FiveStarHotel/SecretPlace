from fastapi import APIRouter

from app.service import check_health as health_service

router = APIRouter()

@router.get("/health")
def check_health():
    return health_service.check_health()