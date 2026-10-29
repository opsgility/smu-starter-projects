-- Up Migration

CREATE TABLE users (
  id              SERIAL PRIMARY KEY,
  email           TEXT    NOT NULL UNIQUE,
  display_name    TEXT    NOT NULL,
  password_hash   TEXT,
  github_user_id  BIGINT  UNIQUE,
  email_verified  BOOLEAN NOT NULL DEFAULT FALSE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Down Migration

DROP TABLE users;
