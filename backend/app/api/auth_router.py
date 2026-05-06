"""認証APIのルーター。"""

from fastapi import APIRouter, Depends, HTTPException, status

from ..api.depends import get_auth_service
from ..schemas.auth_schemas import LoginRequest, LoginResponse
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResponse:
    """メールアドレスとパスワードでログインし、アクセストークンを返す。"""
    try:
        return auth_service.login(email=payload.email, password=payload.password)
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_401_UNAUTHORIZED if detail == "invalid credentials" else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=detail) from exc
