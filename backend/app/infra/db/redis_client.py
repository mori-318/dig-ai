import os

import redis


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        raise RuntimeError(f"Environment variable {name} is required")
    return value


def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be an integer: {value}") from exc


def create_redis_client() -> redis.Redis:
    """redisクライアントを作成"""
    host = _get_required_env("REDIS_HOST")
    port = _get_int_env("REDIS_PORT", 6379)
    db = _get_int_env("REDIS_DB", 0)
    password = os.getenv("REDIS_PASSWORD")

    return redis.Redis(
        host=host,
        port=port,
        db=db,
        password=password,
        socket_connect_timeout=5,
        socket_timeout=5,
    )
