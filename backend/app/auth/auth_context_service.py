"""認証コンテキストの解決と認可判定を行うサービス。"""

from fastapi import HTTPException, status

from ..auth.security import TokenDecodeError, decode_access_token
from ..repositories.user_repository import UserRepository


class AuthContextService:
    """トークンから現在ユーザーを解決し、権限判定を行うサービス。"""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def resolve_current_user(self, token: str):
        """Bearerトークンを検証し、現在ユーザーを返す。"""
        try:
            payload = decode_access_token(token)
        except TokenDecodeError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

        user_id_raw = payload.get("sub")
        try:
            user_id = int(user_id_raw)
        except (TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token subject",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

        user = self.user_repository.find_by_id(user_id)
        if user is None or not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def ensure_admin(self, user):
        """管理者ユーザーかを検証する。"""
        if user["role"] != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="admin privilege required",
            )
        return user
