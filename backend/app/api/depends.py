"""FastAPIルーターで共有する依存関係プロバイダー。"""

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from ..auth.auth_context_service import (
    AdminPrivilegeRequiredError,
    AuthContextService,
    InvalidTokenError,
    InvalidTokenSubjectError,
    UserNotFoundOrInactiveError,
)
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


def get_auth_context_service(request: Request) -> AuthContextService:
    """リクエストごとにAuthContextServiceを生成して返す依存関数。"""
    return _build_auth_context_service(request)


def get_bearer_token(token: str = Depends(oauth2_scheme)) -> str:
    """AuthorizationヘッダーからBearerトークン文字列を取得する依存関数。"""
    return token


def get_current_user(
    auth_context_service: AuthContextService = Depends(get_auth_context_service),
    token: str = Depends(get_bearer_token),
):
    """現在ユーザーを取得し、認証エラーを401に変換する。"""
    try:
        return auth_context_service.resolve_current_user(token)
    except (InvalidTokenError, InvalidTokenSubjectError, UserNotFoundOrInactiveError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def require_admin(
    auth_context_service: AuthContextService = Depends(get_auth_context_service),
    current_user=Depends(get_current_user),
):
    """管理者ユーザーを要求し、権限エラーを403に変換する。"""
    try:
        return auth_context_service.ensure_admin(current_user)
    except AdminPrivilegeRequiredError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
