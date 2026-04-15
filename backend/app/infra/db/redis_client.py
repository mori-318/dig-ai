"""Redisクライアント生成と環境変数解決のヘルパー。"""

import os

import redis


def _get_required_env(name: str) -> str:
    """必須環境変数を取得する。

    Args:
        name (str): 環境変数名。

    Returns:
        str: 環境変数の値。

    Raises:
        RuntimeError: 環境変数が未設定または空文字の場合。
    """
    value = os.getenv(name)
    if value is None or value == "":
        raise RuntimeError(f"Environment variable {name} is required")
    return value


def _get_int_env(name: str, default: int) -> int:
    """整数値の環境変数を取得する。

    Args:
        name (str): 環境変数名。
        default (int): 未設定時に返す既定値。

    Returns:
        int: 取得した整数値または既定値。

    Raises:
        RuntimeError: 設定値を整数へ変換できない場合。
    """
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
