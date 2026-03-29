class CategoryRepository:
    """カテゴリ情報を管理するリポジトリクラス。"""

    def __init__(self, mysql_client):
        self.mysql_client = mysql_client

    def find_by_name(self, name: str) -> dict | None:
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
        return result

    def find_id_by_name(self, name: str) -> int | None:
        """カテゴリ名からカテゴリIDを取得する。"""
        category = self.find_by_name(name)
        return category["id"] if category else None

    def create_category(self, name: str) -> dict:
        """カテゴリを作成して作成結果を返す。"""
        insert_sql = """
        INSERT INTO categories (name)
        VALUES (%s)
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(insert_sql, (name,))
            category_id = cursor.lastrowid
        self.mysql_client.commit()

        select_sql = """
        SELECT id, name, created_at
        FROM categories
        WHERE id = %s
        LIMIT 1
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(select_sql, (category_id,))
            result = cursor.fetchone()
        return result
