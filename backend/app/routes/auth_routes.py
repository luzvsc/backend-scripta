from fastapi import APIRouter, HTTPException, Depends
from app.models.auth import (LoginRequest, TokenResponse)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse, status_code=200, responses={401: {"description": "Email ou senha inválidos"}})
def login(payload: LoginRequest):

    
    try:
        return auth_service.login(payload)

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )