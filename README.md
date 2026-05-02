# Dig AI

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=000)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

古着の写真をアップロードし、AIで査定するアプリケーションです。
管理者向けのアイテム情報登録画面も備えています。

## 📌 開発背景

古着が好きでも、知識や経験の差で「良い一着を見つける（ディグる）」難易度は大きく変わります。
特にマイルドな古着好きの人々にとっては、価格の妥当性や選ぶ根拠が分かりにくく、購買体験のハードルになりがちです。

Dig AI は、このギャップを埋めるために生まれました。
写真をもとにAIが査定金額・査定理由まで返すことで、ディグるための判断軸を提供し、古着選びをもっと気軽に楽しくすることを目指しています。

## 📈 現在の進捗

- プロトタイプとして、バックエンドの基本的な査定アルゴリズム、そして、査定を体験するためのフロントエンドUIが完成している。
- 今後、簡易的にデプロイまで行い、古着好きの知人に使用してもらい、フィードバックをもらう予定である。
- フィードバックが好意的で、かつサービスとして運営していくビジネスプランがしっかり固まれば、サービス化を目指して開発を進めていく。

## 🔍 簡単な査定の流れ

1. ユーザーが査定画面から古着画像をアップロードする。
2. AIが画像からブランド・カテゴリを抽出し、情報不足なら再撮影を案内する。
3. ブランド・カテゴリが取得できた場合、DBから類似商品の情報を検索する。
4. 類似商品の特徴・査定情報と入力画像をもとに、AIが査定価格と理由を生成する。
5. フロントエンドに「査定結果」または「再撮影メッセージ」を返す。

## 🧱 技術スタック

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

## 🧩 主な機能

- 査定機能（`/appraisal/`）
  - 画像アップロードによる査定
  - 査定結果の返却（ブランド・カテゴリ・価格・理由）
  - 再撮影（retake）フロー
- 管理者機能（`/admin/items/`）
  - 古着アイテムの登録

## 🗂️ ディレクトリ構成

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

## ⚙️ セットアップ

### 前提

- Docker / Docker Compose

### 環境変数

リポジトリルートの `.env.example` をコピーして `.env` を作成してください。

```bash
cp .env.example .env
```

用途別にセクション分けしています。

- `Backend (Appraisal)`: 査定機能（`/appraisal`）で必要（`GEMINI_API_KEY`）
- `MySQL (Container bootstrap)`: MySQLコンテナ初期化で使用
- `Backend runtime`: backendコンテナ接続情報で使用
- `Frontend`: frontendコンテナで使用

### Dockerで起動（推奨）

```bash
docker compose up -d
```

起動後のアクセス先:

- フロントエンド: `http://localhost:5173`
- バックエンドAPI: `http://localhost:8001`
  - バックエンドAPIドキュメント（FastAPI自動生成）: `http://localhost:8001/docs`
- MySQL: `localhost:3306`
- Redis: `localhost:6379`

Frontendのページパス:

- 査定ページ: `/`
- 管理者ページ: `/admin`

初期化からやり直す場合:

```bash
docker compose down -v
docker compose up -d
```

## 🗃️ DBマイグレーション

`backend/migrations` 配下のSQLは、Docker初回起動時に自動適用されます。

- `202603241024_init_tables.sql`: テーブル作成
- `202604110001_seed_brands_categories.sql`: 初期ブランド/カテゴリ投入

`backend/sql` は手動投入用（テストデータ等）です。
