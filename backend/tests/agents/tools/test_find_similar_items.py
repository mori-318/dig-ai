import pytest
from dotenv import load_dotenv

from app.agents.tools.find_similar_items import find_similar_items
from app.infra.db import create_mysql_client
from app.repositories.brand_repository import BrandRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.item_repository import ItemRepository

load_dotenv()


@pytest.fixture
def item_repository():
    """テスト用のItemRepositoryインスタンスを提供するpytestフィクスチャ。"""
    mysql_client = create_mysql_client(database="dig_ai_db_test")
    repository = ItemRepository(mysql_client)
    yield repository
    mysql_client.close()


@pytest.fixture
def brand_repository():
    """テスト用のBrandRepositoryインスタンスを提供するpytestフィクスチャ。"""
    mysql_client = create_mysql_client(database="dig_ai_db_test")
    repository = BrandRepository(mysql_client)
    yield repository
    mysql_client.close()


@pytest.fixture
def category_repository():
    """テスト用のCategoryRepositoryインスタンスを提供するpytestフィクスチャ。"""
    mysql_client = create_mysql_client(database="dig_ai_db_test")
    repository = CategoryRepository(mysql_client)
    yield repository
    mysql_client.close()


def test_find_similar_items_with_existing_brand_and_category(
    item_repository, brand_repository, category_repository
):
    """ブランドとカテゴリが存在する場合のfind_similar_items関数のテスト。"""

    brand = "Brand A"  # 存在するブランド名
    category = "Category X"  # 存在するカテゴリ名

    similar_items = find_similar_items(
        brand=brand,
        category=category,
        item_repository=item_repository,
        brand_repository=brand_repository,
        category_repository=category_repository,
    )

    assert isinstance(similar_items, list)
    for item in similar_items:
        assert "features_text" in item
        assert "appraisal_text" in item
        assert "price" in item


def test_find_similar_items_with_nonexistent_brand_or_category(
    item_repository, brand_repository, category_repository
):
    """ブランドまたはカテゴリが存在しない場合のfind_similar_items関数のテスト。"""

    brand = "存在しないブランド"  # 存在しないブランド名
    category = "存在しないカテゴリ"  # 存在しないカテゴリ名

    similar_items = find_similar_items(
        brand=brand,
        category=category,
        item_repository=item_repository,
        brand_repository=brand_repository,
        category_repository=category_repository,
    )

    assert isinstance(similar_items, list)
    assert len(similar_items) == 0
