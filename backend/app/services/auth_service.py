"""認証ユースケースを扱うサービス層。"""

from ..auth.security import create_access_token, verify_password
from ..schemas.auth_schemas import LoginResponse


class AuthService:
    """ログイン処理を提供するサービスクラス。"""

    def __init__(self, user_repository):
        """認証サービスの依存オブジェクトを初期化する。

        Args:
            user_repository: ユーザー情報を扱うリポジトリ。
        """
        self.user_repository = user_repository

    def login(self, *, email: str, password: str) -> LoginResponse:
        """メールアドレスとパスワードを検証してアクセストークンを返す。"""
        normalized_email = email.strip().lower()
        user = self.user_repository.find_by_email(normalized_email)
        if user is None:
            raise ValueError("invalid credentials")
        if not user["is_active"]:
            raise ValueError("user is inactive")
        if not verify_password(password, user["password_hash"]):
            raise ValueError("invalid credentials")

        access_token = create_access_token(
            user_id=user["id"],
            role=user["role"],
            email=user["email"],
        )
        return LoginResponse(access_token=access_token)
