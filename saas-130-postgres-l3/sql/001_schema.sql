-- Lesson 2 end-state schema: three related tables, with every constraint
-- in the database — not in handler code. Lesson 3 converts this into a chain
-- of numbered migrations.

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS trail_items;
DROP TABLE IF EXISTS users;

-- Users of Lumen Trail. The `email` has a UNIQUE constraint so two accounts
-- can never collide on sign-in.
CREATE TABLE users (
  id            SERIAL PRIMARY KEY,
  email         TEXT    NOT NULL UNIQUE,
  display_name  TEXT    NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Trail items in the catalog. Every item is owned by a specific user (the seller).
-- The seller_id foreign key means: Postgres will refuse to insert a trail_item
-- that references a user who doesn't exist, and will refuse to delete a user
-- who still has trail_items on the market.
CREATE TABLE trail_items (
  id            SERIAL PRIMARY KEY,
  seller_id     INTEGER NOT NULL REFERENCES users(id),
  name          TEXT    NOT NULL,
  price_cents   INTEGER NOT NULL CHECK (price_cents >= 0),
  inventory     INTEGER NOT NULL DEFAULT 0 CHECK (inventory >= 0),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Orders. Each order references the user who placed it and the item they bought.
CREATE TABLE orders (
  id            SERIAL PRIMARY KEY,
  buyer_id      INTEGER NOT NULL REFERENCES users(id),
  item_id       INTEGER NOT NULL REFERENCES trail_items(id),
  quantity      INTEGER NOT NULL CHECK (quantity > 0),
  total_cents   INTEGER NOT NULL CHECK (total_cents >= 0),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Seed data: three users, a few items, a few orders. Enough to run JOIN queries.
INSERT INTO users (email, display_name) VALUES
  ('alex@lumentrail.example.com',  'Alex Rivera'),
  ('sam@lumentrail.example.com',   'Sam Chen'),
  ('taylor@lumentrail.example.com','Taylor Nguyen');

INSERT INTO trail_items (seller_id, name, price_cents, inventory) VALUES
  (1, 'Trail Mix',         799,  120),
  (1, 'Camping Lantern',   1999, 25),
  (2, 'Rain Jacket',       8999, 8),
  (2, 'Compass',           2500, 40),
  (3, 'Snow Shovel',       3999, 5);

INSERT INTO orders (buyer_id, item_id, quantity, total_cents) VALUES
  (2, 1, 3, 2397),
  (3, 3, 1, 8999),
  (1, 4, 2, 5000);
