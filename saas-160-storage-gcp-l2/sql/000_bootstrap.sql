-- Minimal upstream tables the photos table FK references. Each lab starts
-- fresh, so a bare SAAS-160 lab needs these even though a full curriculum
-- run already has them from SAAS-130/SAAS-150. IF NOT EXISTS keeps it safe
-- when they're already there.

CREATE TABLE IF NOT EXISTS trail_items (
  id            SERIAL PRIMARY KEY,
  slug          TEXT NOT NULL UNIQUE,
  name          TEXT NOT NULL,
  description   TEXT NOT NULL DEFAULT '',
  price_cents   INTEGER NOT NULL DEFAULT 0,
  rating        NUMERIC(2,1) NOT NULL DEFAULT 0,
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
  id            SERIAL PRIMARY KEY,
  email         TEXT NOT NULL UNIQUE,
  display_name  TEXT NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO trail_items (slug, name) VALUES
  ('angels-landing', 'Angels Landing'),
  ('half-dome-cables', 'Half Dome Cables'),
  ('kalalau-trail', 'Kalalau Trail')
ON CONFLICT (slug) DO NOTHING;
