from ...repositories.brand_repository import BrandRepository
from ...repositories.category_repository import CategoryRepository
from ...repositories.item_repository import ItemRepository


def find_similar_items(
    brand: str,
    category: str,
    item_repository: ItemRepository,
    brand_repository: BrandRepository,
    category_repository: CategoryRepository,
) -> list[dict]:
    """ブランドとカテゴリに基づいて類似商品を検索するツール関数。"""
    if not brand or not category:
        return []

    brand_id = brand_repository.find_id_by_name(brand.strip())
    if brand_id is None:
        return []

    category_id = category_repository.find_id_by_name(category.strip())
    if category_id is None:
        return []

    similar_items = item_repository.find_items(brand_id=brand_id, category_id=category_id)

    result = []
    for item in similar_items:
        result.append(
            {
                "features_text": item["features_text"],
                "appraisal_text": item["appraisal_text"],
                "price": item["price"],
            }
        )

    return result
