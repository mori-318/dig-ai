from fastapi import Request


def get_redis_client(request: Request):
    """FastAPIのRequestオブジェクトからRedisクライアントを取得する依存関数。"""
    return request.app.state.redis_client


def get_appraisal_agent(request: Request):
    """FastAPIのRequestオブジェクトからAppraisalAgentを取得する依存関数。"""
    return request.app.state.appraisal_agent
