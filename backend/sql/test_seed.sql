-- テスト用データ投入
INSERT INTO brands (name) VALUES
  ('Brand A'),
  ('Brand B');

INSERT INTO categories (name) VALUES
  ('Category X'),
  ('Category Y');

-- brands: 1=Brand A, 2=Brand B
-- categories: 1=Category X, 2=Category Y
INSERT INTO items (
  brand_id,
  category_id,
  name,
  features_text,
  appraisal_text,
  price
) VALUES
  (1, 1, 'Item AX-1', 'Feature A1', 'Appraisal A1', 1000),
  (1, 2, 'Item AY-1', 'Feature A2', 'Appraisal A2', 1200),
  (2, 1, 'Item BX-1', 'Feature B1', 'Appraisal B1', 900);
