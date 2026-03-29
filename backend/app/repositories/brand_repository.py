class BrandRepository:
    """ブランド情報を管理するリポジトリクラス。"""

    def __init__(self, mysql_client):
        self.mysql_client = mysql_client

    def find_by_name(self, name: str) -> dict | None:
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
        return result

    def find_id_by_name(self, name: str) -> int | None:
        """ブランド名からブランドIDを取得する。"""
        brand = self.find_by_name(name)
        return brand["id"] if brand else None

    def create_brand(self, name: str) -> dict:
        """ブランドを作成して作成結果を返す。"""
        insert_sql = """
        INSERT INTO brands (name)
        VALUES (%s)
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(insert_sql, (name,))
            brand_id = cursor.lastrowid
        self.mysql_client.commit()

        select_sql = """
        SELECT id, name, created_at
        FROM brands
        WHERE id = %s
        LIMIT 1
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(select_sql, (brand_id,))
            result = cursor.fetchone()
        return result
