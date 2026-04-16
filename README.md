# Dig AI

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=000)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

古着の写真をアップロードし、AIで査定するアプリケーションです。
管理者向けのアイテム情報登録画面も備えています。

## 技術スタック

### バックエンド

- Python / FastAPI: 型安全にAPIを構築しやすく、実装と保守のスピードを両立しやすいため。

### フロントエンド

- TypeScript / React: コンポーネント再利用と型チェックにより、UIの変更を安全に進めやすいため。
- Vite / Tailwind CSS: 開発サイクルが速く、画面実装を短時間で反復できるため。

### DB

- MySQL: 構造化データを安定して扱え、運用実績が豊富なため。
- Redis: インラインDBで、査定状態の一時管理など、低レイテンシなアクセスが必要な処理に適しているため。

### AIエージェント

- Google GenAI SDK（使用モデル: `gemini-2.5-flash-lite`）: まずは、LangGraphなどのフレームワークを使わないでLLMエージェントを実装し、エージェントの仕組みについての理解を深め、かつフレームワークなしで実装する難しさを身をもって体験するために、Google GenAI SDKのみでエージェントの実装を行った。

### 環境構築

- Docker Compose: API・DB・Redisを同じ手順で再現でき、環境差分を減らせるため。
- uv / pnpm: 依存関係の解決が速く、使用経験もあるため。

## 主な機能

- 査定機能（`/appraisal/`）
  - 画像アップロードによる査定
  - 査定結果の返却（ブランド・カテゴリ・価格・理由）
  - 再撮影（retake）フロー
- 管理者機能（`/admin/items/`）
  - 古着アイテムの登録

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
└── frontend/
    └── src/
        ├── features/
        ├── pages/
        └── services/
```

## セットアップ

### 前提

- Docker / Docker Compose

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
- `GET /admin/items/brands/suggest` - 途中までの入力でブランド候補取得（アイテム登録補助）
- `GET /admin/items/categories/suggest` - 途中までの入力でカテゴリ候補取得（アイテム登録補助）
- `POST /admin/items/categories` - カテゴリ作成

## 現在の進捗

- 査定APIと管理者向けAPIの基本実装
- 管理者画面（登録フォーム + サジェストUI）実装
- 査定画面（画像アップロード + 結果表示）実装
- MySQL/Redisを含むDocker開発環境を整備
