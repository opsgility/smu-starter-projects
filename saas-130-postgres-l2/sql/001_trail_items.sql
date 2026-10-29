-- Lesson 1 end-state schema: a single trail_items table.
-- Lesson 2 replaces this with the full three-table design (users, items, orders).

DROP TABLE IF EXISTS trail_items;

CREATE TABLE trail_items (
  id            SERIAL PRIMARY KEY,
  name          TEXT    NOT NULL,
  price_cents   INTEGER NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO trail_items (name, price_cents) VALUES
  ('Trail Mix',         799),
  ('Rain Jacket',       8999),
  ('Camping Lantern',   1999),
  ('Compass',           2500),
  ('Snow Shovel',       3999);
