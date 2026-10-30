from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependency import SessionDep
from app.schemas import RefreshRequest, Token, UserCreate, UserRead
from app.service import auth as auth_service

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(data: UserCreate, session: SessionDep):
    return auth_service.register(data, session)

@router.post("/login", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    return auth_service.login(form.username, form.password, session)

@router.post("/refresh", response_model=Token)
def refresh(payload: RefreshRequest, session: SessionDep):
    return auth_service.refresh_access_token(payload.refresh_token, session)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshRequest, session: SessionDep):
    auth_service.logout(payload.refresh_token, session)

@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
def logout_all(payload: RefreshRequest, session: SessionDep):
    auth_service.logout_all(payload.refresh_token, session)
