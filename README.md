# Dig AI

古着の写真をアップロードし、AIで査定するアプリケーションです。
管理者向けのアイテム登録画面も備えています。

## 技術スタック

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)
![uv](https://img.shields.io/badge/uv-Package%20Manager-2A5BFF)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=000)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.2-06B6D4?logo=tailwindcss&logoColor=white)
![pnpm](https://img.shields.io/badge/pnpm-Frontend-F69220?logo=pnpm&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-Local_Dev-2496ED?logo=docker&logoColor=white)

## 主な機能

- 査定機能（`/appraisal/`）
  - 画像アップロードによる査定
  - 査定結果の返却（ブランド・カテゴリ・価格・理由）
  - 再撮影（retake）フロー
- 管理者機能（`/admin/items/`）
  - 古着アイテムの登録
  - ブランド/カテゴリのサジェスト
  - ブランド/カテゴリの追加

## ディレクトリ構成

```text
dig-ai/
├── AGENTS.md
├── README.md
├── docker-compose.yml
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── sql/
│   └── tests/
├── docs/
│   └── spec/
└── frontend/
    └── src/
        ├── features/
        ├── pages/
        └── services/
```

## セットアップ

### 前提

- Docker / Docker Compose
- またはローカル実行の場合:
  - Python 3.12+
  - `uv`
  - Node.js
  - `pnpm`

### Dockerで起動（推奨）

```bash
docker compose up -d
```

起動後のアクセス先:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8001`
- MySQL: `localhost:3306`
- Redis: `localhost:6379`

初期化からやり直す場合:

```bash
docker compose down -v
docker compose up -d
```

## ローカル開発

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

## DBマイグレーション

`backend/migrations` 配下のSQLは、Docker初回起動時に自動適用されます。

- `202603241024_init_tables.sql`: テーブル作成
- `202604110001_seed_brands_categories.sql`: 初期ブランド/カテゴリ投入

`backend/sql` は手動投入用（テストデータ等）です。

## テスト

### Backend

```bash
cd backend
uv run pytest
```

## APIエンドポイント（抜粋）

- `GET /` - ヘルス/概要
- `POST /appraisal/` - 査定開始
- `POST /appraisal/{appraisal_id}/retake` - 再撮影して再査定
- `POST /admin/items/` - アイテム登録
- `GET /admin/items/brands/suggest` - ブランド候補
- `POST /admin/items/brands` - ブランド作成
- `GET /admin/items/categories/suggest` - カテゴリ候補
- `POST /admin/items/categories` - カテゴリ作成

## 現在の進捗

- 査定APIと管理者向けAPIの基本実装
- 管理者画面（登録フォーム + サジェストUI）実装
- 査定画面（画像アップロード + 結果表示）実装
- MySQL/Redisを含むDocker開発環境を整備
