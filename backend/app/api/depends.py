"""FastAPIルーターで共有する依存関係プロバイダー。"""

from fastapi import Request

from ..container import build_admin_item_service, build_auth_service
from ..services.admin_item_service import AdminItemService
from ..services.auth_service import AuthService
from ..services.appraisal_service import AppraisalService


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


def get_appraisal_service(request: Request) -> AppraisalService:
    """リクエストごとにAppraisalServiceを生成して返す依存関数。"""
    appraisal_agent = get_appraisal_agent(request)
    return AppraisalService(appraisal_agent=appraisal_agent)


def get_appraisal_state_manager(request: Request):
    """FastAPIのRequestオブジェクトからAppraisalStateManagerを取得する依存関数。"""
    return request.app.state.appraisal_state_manager


def get_auth_service(request: Request) -> AuthService:
    """リクエストごとにAuthServiceを生成して返す依存関数。"""
    mysql_client = get_mysql_client(request)
    return build_auth_service(mysql_client)
