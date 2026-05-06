"""認証APIで利用するスキーマ定義。"""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """ログインリクエスト。"""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginResponse(BaseModel):
    """ログインレスポンス。"""

    access_token: str
    token_type: str = "bearer"
