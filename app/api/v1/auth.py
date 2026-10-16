from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependence import SessionDep
from app.schemas import Token, UserCreate, UserRead
from app.service import auth as auth_service

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(data: UserCreate, session: SessionDep):
    return auth_service.register(data, session)

@router.post("/login", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    return auth_service.login(form.username, form.password, session)