"""FastAPIルーターで共有する依存関係プロバイダー。"""

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from ..auth.auth_context_service import AuthContextService
from ..container import build_admin_item_service, build_auth_service
from ..repositories.user_repository import UserRepository
from ..services.admin_item_service import AdminItemService
from ..services.auth_service import AuthService
from ..services.appraisal_service import AppraisalService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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


def _build_auth_context_service(request: Request) -> AuthContextService:
    """AuthContextServiceを生成する内部ヘルパー。"""
    mysql_client = get_mysql_client(request)
    user_repository = UserRepository(mysql_client)
    return AuthContextService(user_repository)


def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    """Bearerトークンを検証し、現在のユーザーを返す依存関数。"""
    auth_context_service = _build_auth_context_service(request)
    return auth_context_service.resolve_current_user(token)


def require_admin(
    request: Request,
    current_user=Depends(get_current_user),
):
    """現在ユーザーが管理者か検証する依存関数。"""
    auth_context_service = _build_auth_context_service(request)
    return auth_context_service.ensure_admin(current_user)
