class ItemRepository:
    """アイテム情報を管理するリポジトリクラス。"""

    def __init__(self, mysql_client):
        self.mysql_client = mysql_client

    def find_items(
        self,
        brand_id: int | None = None,
        category_id: int | None = None,
        top_n: int = 5,
    ) -> list[dict]:
        """条件に合うアイテムをDBから取得するメソッド。
        Args:
            brand_id (int | None): ブランドID。Noneの場合はブランドを条件に含めない。
            category_id (int | None): カテゴリID。Noneの場合はカテゴリを条件に含めない。
            top_n (int): 取得するアイテムの最大数。
        Returns:
            list[dict]: 取得したアイテムのリスト。各アイテムは辞書形式で返される。
        """
        sql = """
        SELECT
            id, brand_id, category_id, name, features_text, appraisal_text,
            price, updated_at, created_at
        FROM items
        WHERE
            (%s IS NULL OR brand_id = %s) AND
            (%s IS NULL OR category_id = %s)
        ORDER BY updated_at DESC
        LIMIT %s
        """
        params = (brand_id, brand_id, category_id, category_id, top_n)
        with self.mysql_client.cursor() as cursor:
            cursor.execute(sql, params)
            results = list(cursor.fetchall())
        return results

    def create_item(
        self,
        brand_id: int,
        category_id: int,
        name: str,
        features_text: str = "",
        appraisal_text: str = "",
        price: int | None = None,
    ) -> dict:
        """アイテムを作成して作成結果を返す。"""
        insert_sql = """
        INSERT INTO items (brand_id, category_id, name, features_text, appraisal_text, price)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (brand_id, category_id, name, features_text, appraisal_text, price)
        with self.mysql_client.cursor() as cursor:
            cursor.execute(insert_sql, params)
            item_id = cursor.lastrowid
        self.mysql_client.commit()

        select_sql = """
        SELECT
            id, brand_id, category_id, name, features_text, appraisal_text,
            price, updated_at, created_at
        FROM items
        WHERE id = %s
        LIMIT 1
        """
        with self.mysql_client.cursor() as cursor:
            cursor.execute(select_sql, (item_id,))
            result = cursor.fetchone()
        return result
