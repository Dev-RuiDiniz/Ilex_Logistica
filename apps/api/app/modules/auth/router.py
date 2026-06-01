from fastapi import APIRouter, Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.schemas import LoginRequest, RefreshRequest, TokenResponse
from app.modules.auth.service import authenticate_user, build_tokens, refresh_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = authenticate_user(db, payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="credenciais invalidas")
    tokens = build_tokens(user)
    return TokenResponse(**tokens)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest) -> TokenResponse:
    try:
        tokens = refresh_access_token(payload.refresh_token)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token invalido") from exc
    if tokens is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token invalido")
    return TokenResponse(**tokens)
