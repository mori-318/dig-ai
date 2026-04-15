# バックエンド リファクタリング候補

## チェックリスト

- [x] 1. 命名とモジュール整理（最優先）

- `appraisal_agent.py` のスペルミスが import 全体に波及していて、保守性が落ちている。
- 対象:
  - `backend/app/agents/appraisal_agent/appraisal_agent.py`
  - `backend/app/agents/__init__.py`

- [x] 2. API 層の責務分離

- ルーター内で `AppraisalService` を毎回直接生成しており DI が不統一（admin 側は `Depends`）。
- `retake` API がダミー返却のままで、実装境界が曖昧。
- 対象:
  - `backend/app/api/appraisal_router.py`
  - `backend/app/api/depends.py`

- [x] 3. 型安全化（dict 境界の縮小）

- `service/repository/agent` 間が `dict` 前提でつながっており、変更に弱い。
- Pydantic / TypedDict / DTO で内部 I/O を固定すると、壊れ方が早期に検知できる。
- 対象:
  - `backend/app/services/appraisal_service.py`
  - `backend/app/repositories/item_repository.py`
  - `backend/app/agents/tools/find_similar_items.py`

- [x] 4. 状態管理の整合性

- `AppraisalAgent` が `done` を返すケースで Redis `delete` と `set` が混在し、ステート運用ルールが一貫していない。
- `processing` 状態の寿命・再開条件を仕様化してコードへ反映すべき。
- 対象:
  - `backend/app/agents/appraisal_agent/appraisal_agent.py`
  - `backend/app/services/appraisal_state_manager.py`

- [ ] 5. DB / 設定の初期化設計

- 環境変数未設定時のバリデーションが薄く、起動時エラーが遅延する。
- トランザクション / commit の扱いが repository ごとに散在。
- 対象:
  - `backend/app/infra/db/mysql_client.py`
  - `backend/app/infra/db/redis_client.py`

- [x] 6. ドキュメントと実体のズレ修正

- README が `backend/sql/init_tables.sql` を参照しているが現状存在せず、運用ミスの原因になる。
- 対象:
  - `backend/README.md`
  - `backend/migrations/*`

## 着手順

効果と安全性のバランスから、まずは `1 -> 2 -> 3` の順で進める。
