-- Up Migration

CREATE TABLE orders (
  id            SERIAL PRIMARY KEY,
  buyer_id      INTEGER NOT NULL REFERENCES users(id),
  item_id       INTEGER NOT NULL REFERENCES trail_items(id),
  quantity      INTEGER NOT NULL CHECK (quantity > 0),
  total_cents   INTEGER NOT NULL CHECK (total_cents >= 0),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Down Migration

DROP TABLE orders;
