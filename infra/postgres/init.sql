CREATE TABLE IF NOT EXISTS categories (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

INSERT INTO categories (name) VALUES
  ('groceries'),
  ('dining'),
  ('travel'),
  ('transport'),
  ('entertainment'),
  ('shopping'),
  ('utilities'),
  ('health'),
  ('other')
ON CONFLICT (name) DO NOTHING;
