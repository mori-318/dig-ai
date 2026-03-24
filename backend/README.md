# バックエンド

## 環境構築手順

## DBマイグレーション
```bash
mysql -h <HOST> -P <PORT> -u <USER> -p <PASSWORD> <DB_NAME> < backend/sql/init_tables.sql
```