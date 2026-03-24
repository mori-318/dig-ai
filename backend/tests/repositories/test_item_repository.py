import pytest
from dotenv import load_dotenv

from app.infra.db import create_mysql_client
from app.repositories.item_repository import ItemRepository

load_dotenv()


@pytest.fixture
def item_repository():
    """テスト用のItemRepositoryインスタンスを提供するpytestフィクスチャ。"""
    mysql_client = create_mysql_client(database="dig_ai_db_test")
    repository = ItemRepository(mysql_client)
    yield repository
    mysql_client.close()


def test_find_items_with_existing_brand_and_category(item_repository):
    """ブランドIDとカテゴリIDでアイテムを取得できること。"""
    brand_id = 1
    category_id = 2

    items = item_repository.find_items(brand_id=brand_id, category_id=category_id, top_n=5)

    assert isinstance(items, list)
    assert len(items) <= 5
    for item in items:
        assert "id" in item
        assert "brand_id" in item
        assert "category_id" in item
        assert "name" in item
        assert "features_text" in item
        assert "appraisal_text" in item
        assert "price" in item
        assert "updated_at" in item
        assert "created_at" in item


def test_find_items_with_nonexistent_brand_or_category(item_repository):
    """存在しない条件では空リストになること。"""
    items = item_repository.find_items(brand_id=9999, category_id=9999, top_n=5)

    assert isinstance(items, list)
    assert len(items) == 0
