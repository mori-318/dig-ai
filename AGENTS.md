# AGENTS.md

古着をAIで査定するアプリであるDig AIの開発を行うリポジトリ

## ディレクトリ構造

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

## コーディング

- 層の分離・可読性・保守性を意識したコーディング・設計を行う

## バックエンド開発

- uvを使用している（uv run ..）

## フロントエンド

- pnpmを使用している