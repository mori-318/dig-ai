-- Test seed for local Docker initialization
-- This file is executed only on first MySQL container initialization

SET NAMES utf8mb4;

INSERT INTO brands (name) VALUES
  ('Levi''s'),
  ('Nike'),
  ('adidas'),
  ('Carhartt'),
  ('Patagonia'),
  ('The North Face'),
  ('Champion'),
  ('Ralph Lauren'),
  ('Burberry'),
  ('Uniqlo');

INSERT INTO categories (name) VALUES
  ('Tシャツ'),
  ('シャツ'),
  ('パーカー'),
  ('ニット'),
  ('デニムジャケット'),
  ('レザージャケット'),
  ('コート'),
  ('ジーンズ'),
  ('スニーカー'),
  ('バッグ');
