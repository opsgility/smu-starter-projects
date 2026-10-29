-- Up Migration

CREATE TABLE trail_items (
  id            SERIAL PRIMARY KEY,
  seller_id     INTEGER NOT NULL REFERENCES users(id),
  name          TEXT    NOT NULL,
  price_cents   INTEGER NOT NULL CHECK (price_cents >= 0),
  inventory     INTEGER NOT NULL DEFAULT 0 CHECK (inventory >= 0),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Down Migration

DROP TABLE trail_items;
