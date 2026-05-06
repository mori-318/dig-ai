"""認証セキュリティ（パスワードハッシュ・JWT生成/検証）。"""

import os
from typing import Any
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenDecodeError(Exception):
    """トークンのデコードエラー。"""


def _get_secret_key() -> str:
    """JWTのシークレットキーを取得する。環境変数から取得し、存在しない場合は例外を投げる。"""
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise ValueError("JWT_SECRET_KEY environment variable is not set.")
    return secret_key


def get_access_token_expire_minutes() -> int:
    raw = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    try:
        minutes = int(raw)
    except ValueError as exc:
        raise RuntimeError(f"Invalid JWT_ACCESS_TOKEN_EXPIRE_MINUTES: {raw}") from exc
    if minutes <= 0:
        raise RuntimeError(f"JWT_ACCESS_TOKEN_EXPIRE_MINUTES must be positive: {raw}")
    return minutes


def hash_password(password: str) -> str:
    """パスワードをハッシュ化する。"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """平文のパスワードとハッシュ化されたパスワードを検証する。"""
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(*, user_id: int, role: str, email: str) -> str:
    """アクセストークンを生成する。"""
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=get_access_token_expire_minutes())

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "email": email,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, _get_secret_key(), algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """アクセストークンをデコードする。"""
    try:
        payload = jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
    except JWTError as exc:
        raise TokenDecodeError("Invalid token") from exc

    if payload.get("type") != "access":
        raise TokenDecodeError("Invalid token type")
    if "sub" not in payload or "role" not in payload:
        raise TokenDecodeError("Invalid token payload")
    return payload
