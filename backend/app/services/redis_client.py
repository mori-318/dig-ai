import os

import redis


def create_redis_client():
    """redisクライアントを作成"""
    host = os.getenv("REDIS_HOST")
    port = int(os.getenv("REDIS_PORT"))
    db = int(os.getenv("REDIS_DB"))
    password = os.getenv("REDIS_PASSWORD")

    return redis.Redis(host=host, port=port, db=db, password=password)
