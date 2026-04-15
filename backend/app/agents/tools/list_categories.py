"""利用可能なカテゴリ一覧を取得するツール。"""

from ...repositories.category_repository import CategoryRepository


def list_categories(category_repository: CategoryRepository) -> list[str]:
    """カテゴリのリストを取得するツール関数。"""
    categories = category_repository.list_categories()
    return [category["name"] for category in categories]
