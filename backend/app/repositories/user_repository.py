"""ユーザー情報へのデータアクセスを提供するリポジトリ。"""

from typing import cast

from ..schemas.internal_types import UserRecord


class UserRepository:
    """ユーザー情報を管理するリポジトリクラス。"""

    def __init__(self, mysql_client):
        """ユーザーリポジトリの依存オブジェクトを初期化する。

        Args:
            mysql_client: MySQL接続クライアント。
        """
        self.mysql_client = mysql_client

    def find_by_email(self, email: str) -> UserRecord | None:
        """メールアドレスからユーザー情報を取得する。"""
        sql = """
        SELECT id, email, password_hash, role, is_active, created_at, updated_at
        FROM users
        WHERE email = %s
        LIMIT 1
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
        if result is None:
            return None
        return cast(UserRecord, result)

    def find_by_id(self, user_id: int) -> UserRecord | None:
        """ユーザーIDからユーザー情報を取得する。"""
        sql = """
        SELECT id, email, password_hash, role, is_active, created_at, updated_at
        FROM users
        WHERE id = %s
        LIMIT 1
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
        if result is None:
            return None
        return cast(UserRecord, result)
