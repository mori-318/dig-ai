from fastapi import Request

from ..container import build_admin_item_service
from ..services.admin_item_service import AdminItemService


def get_redis_client(request: Request):
    """FastAPIのRequestオブジェクトからRedisクライアントを取得する依存関数。"""
    return request.app.state.redis_client


def get_mysql_client(request: Request):
    """FastAPIのRequestオブジェクトからMySQLクライアントを取得する依存関数。"""
    return request.app.state.mysql_client


def get_admin_item_service(request: Request) -> AdminItemService:
    """リクエストごとにAdminItemServiceを生成して返す依存関数。"""
    mysql_client = get_mysql_client(request)
    return build_admin_item_service(mysql_client)


def get_appraisal_agent(request: Request):
    """FastAPIのRequestオブジェクトからAppraisalAgentを取得する依存関数。"""
    return request.app.state.appraisal_agent


def get_appraisal_state_manager(request: Request):
    """FastAPIのRequestオブジェクトからAppraisalStateManagerを取得する依存関数。"""
    return request.app.state.appraisal_state_manager
