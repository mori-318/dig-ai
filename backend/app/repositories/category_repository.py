"""カテゴリ情報へのデータアクセスを提供するリポジトリ。"""

from typing import cast

from ..schemas.internal_types import CategoryListItem, CategoryRecord

class CategoryRepository:
    """カテゴリ情報を管理するリポジトリクラス。"""

    def __init__(self, mysql_client):
        """カテゴリリポジトリの依存オブジェクトを初期化する。

        Args:
            mysql_client: MySQL接続クライアント。
        """
        self.mysql_client = mysql_client

    def find_by_name(self, name: str) -> CategoryRecord | None:
        """カテゴリ名からカテゴリ情報を取得する。"""
        sql = """
        SELECT id, name, created_at
        FROM categories
        WHERE name = %s
        LIMIT 1
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
        if result is None:
            return None
        return cast(CategoryRecord, result)

    def find_by_id(self, category_id: int) -> CategoryRecord | None:
        """カテゴリIDからカテゴリ情報を取得する。"""
        sql = """
        SELECT id, name, created_at
        FROM categories
        WHERE id = %s
        LIMIT 1
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(sql, (category_id,))
            result = cursor.fetchone()
        if result is None:
            return None
        return cast(CategoryRecord, result)

    def find_id_by_name(self, name: str) -> int | None:
        """カテゴリ名からカテゴリIDを取得する。"""
        category = self.find_by_name(name)
        return category["id"] if category else None

    def create_category(self, name: str) -> CategoryRecord:
        """カテゴリを作成して作成結果を返す。"""
        insert_sql = """
        INSERT INTO categories (name)
        VALUES (%s)
        """
        try:
            with self.mysql_client.cursor() as cursor:
                cursor.execute(insert_sql, (name,))
                category_id = cursor.lastrowid
            self.mysql_client.commit()
        except Exception:
            self.mysql_client.rollback()
            raise
        created = self.find_by_id(category_id)
        if created is None:
            raise RuntimeError("created category not found")
        return created

    def suggest_categories(self, q: str, limit: int = 20) -> list[CategoryListItem]:
        """入力途中の文字列に一致するカテゴリ候補を返す。"""
        sql = """
        SELECT id, name
        FROM categories
        WHERE name LIKE %s
        ORDER BY name ASC
        LIMIT %s
        """
        like_query = f"%{q}%"
        with self.mysql_client.cursor() as cursor:
            cursor.execute(sql, (like_query, limit))
            results = list(cursor.fetchall())
        return cast(list[CategoryListItem], results)

    def list_categories(self) -> list[CategoryRecord]:
        """すべてのカテゴリを取得する。"""
        sql = """
        SELECT id, name, created_at
        FROM categories
        ORDER BY name ASC
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(sql)
            results = list(cursor.fetchall())
        return cast(list[CategoryRecord], results)
