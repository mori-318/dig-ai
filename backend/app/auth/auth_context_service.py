"""認証コンテキストの解決と認可判定を行うサービス。"""

from ..auth.security import TokenDecodeError, decode_access_token
from ..repositories.user_repository import UserRepository


class AuthContextError(Exception):
    """認証コンテキスト解決時の基底例外。"""


class InvalidTokenError(AuthContextError):
    """トークン検証に失敗したことを示す例外。"""


class InvalidTokenSubjectError(AuthContextError):
    """トークンのsubクレームが不正であることを示す例外。"""


class UserNotFoundOrInactiveError(AuthContextError):
    """ユーザーが見つからない、または無効であることを示す例外。"""


class AdminPrivilegeRequiredError(AuthContextError):
    """管理者権限が必要であることを示す例外。"""


class AuthContextService:
    """トークンから現在ユーザーを解決し、権限判定を行うサービス。"""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def resolve_current_user(self, token: str):
        """Bearerトークンを検証し、現在ユーザーを返す。"""
        try:
            payload = decode_access_token(token)
        except TokenDecodeError as exc:
            raise InvalidTokenError("invalid token") from exc

        user_id_raw = payload.get("sub")
        try:
            user_id = int(user_id_raw)
        except (TypeError, ValueError) as exc:
            raise InvalidTokenSubjectError("invalid token subject") from exc

        user = self.user_repository.find_by_id(user_id)
        if user is None or not user["is_active"]:
            raise UserNotFoundOrInactiveError("user not found or inactive")
        return user

    def ensure_admin(self, user):
        """管理者ユーザーかを検証する。"""
        if user["role"] != "admin":
            raise AdminPrivilegeRequiredError("admin privilege required")
        return user
