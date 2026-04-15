from unittest.mock import MagicMock, patch

import pytest

from app.infra.db.mysql_client import create_mysql_client
from app.infra.db.redis_client import create_redis_client


def test_create_mysql_client_requires_host(monkeypatch):
    monkeypatch.delenv("MYSQL_HOST", raising=False)
    monkeypatch.setenv("MYSQL_USER", "digai")
    monkeypatch.setenv("MYSQL_PASSWORD", "digai")
    monkeypatch.setenv("MYSQL_DATABASE", "dig_ai_db")

    with pytest.raises(RuntimeError, match="MYSQL_HOST"):
        create_mysql_client()


def test_create_mysql_client_validates_port(monkeypatch):
    monkeypatch.setenv("MYSQL_HOST", "localhost")
    monkeypatch.setenv("MYSQL_PORT", "invalid")
    monkeypatch.setenv("MYSQL_USER", "digai")
    monkeypatch.setenv("MYSQL_PASSWORD", "digai")
    monkeypatch.setenv("MYSQL_DATABASE", "dig_ai_db")

    with pytest.raises(RuntimeError, match="MYSQL_PORT"):
        create_mysql_client()


def test_create_mysql_client_uses_defaults(monkeypatch):
    monkeypatch.setenv("MYSQL_HOST", "localhost")
    monkeypatch.delenv("MYSQL_PORT", raising=False)
    monkeypatch.setenv("MYSQL_USER", "digai")
    monkeypatch.setenv("MYSQL_PASSWORD", "digai")
    monkeypatch.setenv("MYSQL_DATABASE", "dig_ai_db")

    with patch("app.infra.db.mysql_client.pymysql.connect", return_value=MagicMock()) as mock_connect:
        create_mysql_client()

    kwargs = mock_connect.call_args.kwargs
    assert kwargs["port"] == 3306
    assert kwargs["autocommit"] is False


def test_create_redis_client_requires_host(monkeypatch):
    monkeypatch.delenv("REDIS_HOST", raising=False)

    with pytest.raises(RuntimeError, match="REDIS_HOST"):
        create_redis_client()


def test_create_redis_client_validates_port(monkeypatch):
    monkeypatch.setenv("REDIS_HOST", "localhost")
    monkeypatch.setenv("REDIS_PORT", "invalid")

    with pytest.raises(RuntimeError, match="REDIS_PORT"):
        create_redis_client()


def test_create_redis_client_uses_defaults(monkeypatch):
    monkeypatch.setenv("REDIS_HOST", "localhost")
    monkeypatch.delenv("REDIS_PORT", raising=False)
    monkeypatch.delenv("REDIS_DB", raising=False)

    with patch("app.infra.db.redis_client.redis.Redis", return_value=MagicMock()) as mock_redis:
        create_redis_client()

    kwargs = mock_redis.call_args.kwargs
    assert kwargs["port"] == 6379
    assert kwargs["db"] == 0
