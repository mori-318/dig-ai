from app.services.admin_item_service import AdminItemService


class DummyItemRepository:
    def __init__(self):
        self.last_create_args = None

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
        self.last_create_args = {
            "brand_id": brand_id,
            "category_id": category_id,
            "name": name,
            "features_text": features_text,
            "appraisal_text": appraisal_text,
            "price": price,
        }
        return {
            "id": 1,
            "brand_id": brand_id,
            "category_id": category_id,
            "name": name,
            "features_text": features_text,
            "appraisal_text": appraisal_text,
            "price": price,
        }


class DummyBrandRepository:
    def __init__(self, existing: dict | None = None):
        self.existing = existing
        self.created_names: list[str] = []

    def find_by_name(self, name: str) -> dict | None:
        return self.existing if self.existing and self.existing["name"] == name else None

    def create_brand(self, name: str) -> dict:
        self.created_names.append(name)
        return {"id": 10, "name": name}


class DummyCategoryRepository:
    def __init__(self, existing: dict | None = None):
        self.existing = existing
        self.created_names: list[str] = []

    def find_by_name(self, name: str) -> dict | None:
        return self.existing if self.existing and self.existing["name"] == name else None

    def create_category(self, name: str) -> dict:
        self.created_names.append(name)
        return {"id": 20, "name": name}


def test_create_item_uses_existing_brand_and_category():
    """既存のブランド・カテゴリがある場合は作成せずにIDを使う。"""
    item_repository = DummyItemRepository()
    brand_repository = DummyBrandRepository(existing={"id": 3, "name": "Levi's"})
    category_repository = DummyCategoryRepository(existing={"id": 4, "name": "ジーンズ"})
    service = AdminItemService(item_repository, brand_repository, category_repository)

    result = service.create_item(
        brand="Levi's",
        category="ジーンズ",
        name="501",
        features_text="ストレート",
        appraisal_text="定番モデル",
        price=9000,
    )

    assert result["brand_id"] == 3
    assert result["category_id"] == 4
    assert brand_repository.created_names == []
    assert category_repository.created_names == []
    assert item_repository.last_create_args is not None
    assert item_repository.last_create_args["brand_id"] == 3
    assert item_repository.last_create_args["category_id"] == 4


def test_create_item_creates_missing_brand_and_category():
    """未登録のブランド・カテゴリは自動作成してIDを使う。"""
    item_repository = DummyItemRepository()
    brand_repository = DummyBrandRepository()
    category_repository = DummyCategoryRepository()
    service = AdminItemService(item_repository, brand_repository, category_repository)

    result = service.create_item(
        brand="Dickies",
        category="ワークパンツ",
        name="874",
        features_text="ワーク定番",
        appraisal_text="需要が安定",
        price=7000,
    )

    assert result["brand_id"] == 10
    assert result["category_id"] == 20
    assert brand_repository.created_names == ["Dickies"]
    assert category_repository.created_names == ["ワークパンツ"]


def test_create_item_raises_when_brand_or_category_is_blank():
    """brand/category が空白のみの場合はエラーにする。"""
    item_repository = DummyItemRepository()
    brand_repository = DummyBrandRepository()
    category_repository = DummyCategoryRepository()
    service = AdminItemService(item_repository, brand_repository, category_repository)

    try:
        service.create_item(
            brand="   ",
            category="ジーンズ",
            name="501",
            features_text="x",
            appraisal_text="y",
            price=1000,
        )
        assert False, "ValueError should be raised for blank brand"
    except ValueError as e:
        assert str(e) == "brand name is required"

    try:
        service.create_item(
            brand="Levi's",
            category="   ",
            name="501",
            features_text="x",
            appraisal_text="y",
            price=1000,
        )
        assert False, "ValueError should be raised for blank category"
    except ValueError as e:
        assert str(e) == "category name is required"
