from dotenv import load_dotenv

from app.infra.db import create_mysql_client
from app.repositories.item_repository import ItemRepository

load_dotenv()


def test_find_items():
    mysql_client = create_mysql_client(database="dig_ai_db_test")
    item_repository = ItemRepository(mysql_client)

    # ブランドIDとカテゴリIDを指定してアイテムを取得
    brand_id = 1  # 例: ブランドID 1
    category_id = 2  # 例: カテゴリID 2
    items = item_repository.find_items(brand_id=brand_id, category_id=category_id, top_n=5)
    print(items)

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

    mysql_client.close()
