from dotenv import load_dotenv

from app.infra.db import create_mysql_client
from app.repositories.brand_repository import BrandRepository

load_dotenv()


def test_find_by_name_existing_brand():
    """存在するブランド名で取得できること。"""
    mysql_client = create_mysql_client(database="dig_ai_db_test")
    repository = BrandRepository(mysql_client)

    brand = repository.find_by_name("Brand A")

    assert brand is not None
    assert brand["name"] == "Brand A"

    mysql_client.close()


def test_find_by_name_nonexistent_brand():
    """存在しないブランド名はNoneになること。"""
    mysql_client = create_mysql_client(database="dig_ai_db_test")
    repository = BrandRepository(mysql_client)

    brand = repository.find_by_name("Nonexistent Brand")

    assert brand is None

    mysql_client.close()
