from fastapi import APIRouter

from app.dependence import SessionDep
from app.schemas import UserCreate, UserRead
from app.service import auth as auth_service

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(data: UserCreate, session: SessionDep):
    return auth_service.register(data, session)