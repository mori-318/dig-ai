-- 管理者ユーザーを手動作成するためのテンプレートSQL（MySQLコンテナ内または接続先クライアントで実行）。
-- 実際の認証情報や平文パスワードはコミットしないこと。
-- 実行前にプレースホルダー値を置き換えること。
INSERT INTO users (email, password_hash, role, is_active)
VALUES (
  'REPLACE_WITH_ADMIN_EMAIL',
  'REPLACE_WITH_BCRYPT_HASH',
  'admin',
  1
)
ON DUPLICATE KEY UPDATE
  role = VALUES(role),
  is_active = VALUES(is_active);
