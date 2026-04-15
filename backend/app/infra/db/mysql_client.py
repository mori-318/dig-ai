import os

import pymysql


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


def create_mysql_client(database: str | None = None) -> pymysql.connections.Connection:
    """mysqlクライアントを作成する関数。"""
    mysql_host = _get_required_env("MYSQL_HOST")
    mysql_port = _get_int_env("MYSQL_PORT", 3306)
    mysql_user = _get_required_env("MYSQL_USER")
    mysql_password = _get_required_env("MYSQL_PASSWORD")
    mysql_database = database or _get_required_env("MYSQL_DATABASE")

    return pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database,
        autocommit=False,
        connect_timeout=10,
        read_timeout=30,
        write_timeout=30,
        charset="utf8mb4",
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor,
    )
