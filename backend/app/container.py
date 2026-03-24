from functools import partial

from .agents import AppraisalAgent
from .agents.tools.find_similar_items import find_similar_items
from .repositories.brand_repository import BrandRepository
from .repositories.category_repository import CategoryRepository
from .repositories.item_repository import ItemRepository
from .services.appraisal_state_manager import AppraisalStateManager


def build_appraisal_agent(mysql_client, state_manager) -> AppraisalAgent:
    """AppraisalAgentを依存関係込みで生成する。"""
    item_repository = ItemRepository(mysql_client)
    brand_repository = BrandRepository(mysql_client)
    category_repository = CategoryRepository(mysql_client)
    find_similar_items_tool = partial(
        find_similar_items,
        item_repository=item_repository,
        brand_repository=brand_repository,
        category_repository=category_repository,
    )
    return AppraisalAgent(
        find_similar_items=find_similar_items_tool,
        state_manager=state_manager,
    )


def build_appraisal_state_manager(redis_client) -> AppraisalStateManager:
    """AppraisalStateManagerを依存関係込みで生成する。"""
    return AppraisalStateManager(redis_client)
