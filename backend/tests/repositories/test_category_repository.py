from dotenv import load_dotenv

from app.infra.db import create_mysql_client
from app.repositories.category_repository import CategoryRepository

load_dotenv()


def test_find_by_name_existing_category():
    """存在するカテゴリ名で取得できること。"""
    mysql_client = create_mysql_client(database="dig_ai_db_test")
    repository = CategoryRepository(mysql_client)

    category = repository.find_by_name("Category X")

    assert category is not None
    assert category["name"] == "Category X"

    mysql_client.close()


def test_find_by_name_nonexistent_category():
    """存在しないカテゴリ名はNoneになること。"""
    mysql_client = create_mysql_client(database="dig_ai_db_test")
    repository = CategoryRepository(mysql_client)

    category = repository.find_by_name("Nonexistent Category")

    assert category is None

    mysql_client.close()
