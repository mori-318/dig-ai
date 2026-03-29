from ...repositories.category_repository import CategoryRepository


def list_categories(category_repository: CategoryRepository) -> list[dict]:
    """カテゴリのリストを取得するツール関数。"""
    return category_repository.list_categories()
