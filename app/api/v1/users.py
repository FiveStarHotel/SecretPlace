from fastapi import APIRouter

from app.dependency import OptionalUserDep
from app.schemas import UserRead

router = APIRouter()

@router.get("/me", response_model=UserRead)
def read_me(current_user: OptionalUserDep):
    if current_user is not None:
        return UserRead.model_validate(current_user)
    
    return UserRead(
        id=-1,
        username="NOT AUTHORIZED"
    )
