"""サービスとエージェントの依存関係を組み立てるヘルパー。"""

from functools import partial

from .agents import AppraisalAgent
from .agents.tools.find_similar_items import find_similar_items
from .agents.tools.list_categories import list_categories
from .repositories.brand_repository import BrandRepository
from .repositories.category_repository import CategoryRepository
from .repositories.item_repository import ItemRepository
from .repositories.user_repository import UserRepository
from .services.admin_item_service import AdminItemService
from .services.auth_service import AuthService
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
    list_categories_tool = partial(
        list_categories,
        category_repository=category_repository,
    )
    return AppraisalAgent(
        find_similar_items=find_similar_items_tool,
        list_categories=list_categories_tool,
        state_manager=state_manager,
    )


def build_appraisal_state_manager(redis_client) -> AppraisalStateManager:
    """AppraisalStateManagerを依存関係込みで生成する。"""
    return AppraisalStateManager(redis_client)


def build_admin_item_service(mysql_client) -> AdminItemService:
    """AdminItemServiceを依存関係込みで生成する。"""
    item_repository = ItemRepository(mysql_client)
    brand_repository = BrandRepository(mysql_client)
    category_repository = CategoryRepository(mysql_client)
    return AdminItemService(item_repository, brand_repository, category_repository)


def build_auth_service(mysql_client) -> AuthService:
    """AuthServiceを依存関係込みで生成する。"""
    user_repository = UserRepository(mysql_client)
    return AuthService(user_repository)
