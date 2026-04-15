"""ブランド情報へのデータアクセスを提供するリポジトリ。"""

from typing import cast

from ..schemas.internal_types import BrandRecord

class BrandRepository:
    """ブランド情報を管理するリポジトリクラス。"""

    def __init__(self, mysql_client):
        """ブランドリポジトリの依存オブジェクトを初期化する。

        Args:
            mysql_client: MySQL接続クライアント。
        """
        self.mysql_client = mysql_client

    def find_by_name(self, name: str) -> BrandRecord | None:
        """ブランド名からブランド情報を取得する。"""
        sql = """
        SELECT id, name, created_at
        FROM brands
        WHERE name = %s
        LIMIT 1
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
        if result is None:
            return None
        return cast(BrandRecord, result)

    def find_by_id(self, brand_id: int) -> BrandRecord | None:
        """ブランドIDからブランド情報を取得する。"""
        sql = """
        SELECT id, name, created_at
        FROM brands
        WHERE id = %s
        LIMIT 1
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(sql, (brand_id,))
            result = cursor.fetchone()
        if result is None:
            return None
        return cast(BrandRecord, result)

    def find_id_by_name(self, name: str) -> int | None:
        """ブランド名からブランドIDを取得する。"""
        brand = self.find_by_name(name)
        return brand["id"] if brand else None

    def create_brand(self, name: str) -> BrandRecord:
        """ブランドを作成して作成結果を返す。"""
        insert_sql = """
        INSERT INTO brands (name)
        VALUES (%s)
        """
        try:
            with self.mysql_client.cursor() as cursor:
                cursor.execute(insert_sql, (name,))
                brand_id = cursor.lastrowid
            self.mysql_client.commit()
        except Exception:
            self.mysql_client.rollback()
            raise
        created = self.find_by_id(brand_id)
        if created is None:
            raise RuntimeError("created brand not found")
        return created

    def suggest_brands(self, q: str, limit: int = 20) -> list[dict]:
        """入力途中の文字列に一致するブランド候補を返す。"""
        sql = """
        SELECT id, name
        FROM brands
        WHERE name LIKE %s
        ORDER BY name ASC
        LIMIT %s
        """
        like_query = f"%{q}%"
        with self.mysql_client.cursor() as cursor:
            cursor.execute(sql, (like_query, limit))
            results = list(cursor.fetchall())
        return results
