from fastapi import APIRouter

from app.dependency import CurrentUserDep, SessionDep
from app.schemas import UserRead

router = APIRouter()

@router.get("/me", response_model=UserRead)
def read_me(current_user: CurrentUserDep, session: SessionDep):
    return UserRead.model_validate(current_user)
