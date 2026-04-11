import os

import pymysql


def create_mysql_client(database: str | None = None):
    """mysqlクライアントを作成する関数。"""
    mysql_host = os.getenv("MYSQL_HOST")
    mysql_port = int(os.getenv("MYSQL_PORT", 3306))
    mysql_user = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_database = database or os.getenv("MYSQL_DATABASE")

    return pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database,
        charset="utf8mb4",
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor,
    )
