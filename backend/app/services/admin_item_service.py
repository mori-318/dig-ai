from ..schemas.admin_item_schemas import Brand, Category


class AdminItemService:
    """管理者向けのアイテム関連のサービスクラス。"""

    def __init__(self, item_repository, brand_repository, category_repository):
        self.item_repository = item_repository
        self.brand_repository = brand_repository
        self.category_repository = category_repository

    def create_item(
        self,
        *,
        brand_id: int,
        category_id: int,
        name: str,
        features_text: str,
        appraisal_text: str,
        price: int | None = None,
    ) -> dict:
        """アイテムを新規作成するメソッド。
        Args:
            brand_id (int): ブランドID。
            category_id (int): カテゴリID。
            name (str): アイテム名。
            features_text (str): アイテムの特徴を説明するテキスト。
            appraisal_text (str): アイテムの査定に関する説明テキスト。
            price (int | None): アイテムの価格。
        Returns:
            dict: 作成されたアイテムの情報を含む辞書。
        """
        return self.item_repository.create_item(
            brand_id=brand_id,
            category_id=category_id,
            name=name,
            features_text=features_text,
            appraisal_text=appraisal_text,
            price=price,
        )

    def suggest_brands(self, q: str, limit: int = 20) -> list[Brand]:
        """入力途中の文字列に基づいてブランドをサジェストするメソッド。"""
        brands = self.brand_repository.suggest_brands(q, limit)
        return [Brand(**brand) for brand in brands]

    def create_brand(self, name: str) -> Brand:
        """ブランドを新規作成するメソッド。"""
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("brand name is required")
        if self.brand_repository.find_by_name(normalized_name) is not None:
            raise ValueError("brand already exists")
        created = self.brand_repository.create_brand(normalized_name)
        return Brand(**created)

    def suggest_categories(self, q: str, limit: int = 20) -> list[Category]:
        """入力途中の文字列に基づいてカテゴリをサジェストするメソッド。"""
        categories = self.category_repository.suggest_categories(q, limit)
        return [Category(**category) for category in categories]

    def create_category(self, name: str) -> Category:
        """カテゴリを新規作成するメソッド。"""
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("category name is required")
        if self.category_repository.find_by_name(normalized_name) is not None:
            raise ValueError("category already exists")
        created = self.category_repository.create_category(normalized_name)
        return Category(**created)
