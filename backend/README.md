# バックエンド

## 環境構築手順

## DBマイグレーション

### Docker利用時（推奨）

`docker-compose.yml` では、MySQLの初期化時に `backend/migrations` 配下のSQLが自動実行される。

- `202603241024_init_tables.sql`: テーブル作成
- `202604110001_seed_brands_categories.sql`: 初期ブランド/カテゴリ投入

初回起動:

```bash
docker compose up -d
```

注意:

- `docker-entrypoint-initdb.d` は「データディレクトリが空のときだけ」実行される。
- 既存データを消して初期化からやり直す場合は、ボリューム削除が必要。

```bash
docker compose down -v
docker compose up -d
```

### 手動実行（Dockerを使わない場合）

マイグレーションはファイル名順で実行する。

```bash
mysql -h <HOST> -P <PORT> -u <USER> -p <DB_NAME> < backend/migrations/202603241024_init_tables.sql
mysql -h <HOST> -P <PORT> -u <USER> -p <DB_NAME> < backend/migrations/202604110001_seed_brands_categories.sql
```

## `migrations` と `sql` の使い分け

- `backend/migrations`
  - 環境初期化に必要な「正」となるSQL。
  - Docker初期化時に自動適用される前提。
- `backend/sql`
  - 手動投入用の補助SQL（テストデータ、追加seedなど）。
  - 自動適用はしない。

例:

```bash
mysql -h <HOST> -P <PORT> -u <USER> -p <DB_NAME> < backend/sql/test_seed.sql
```
