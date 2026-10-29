-- Up Migration

CREATE TABLE email_tokens (
  id          SERIAL      PRIMARY KEY,
  user_id     INTEGER     NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  purpose     TEXT        NOT NULL CHECK (purpose IN ('verify_email', 'password_reset')),
  token_hash  TEXT        NOT NULL,
  expires_at  TIMESTAMPTZ NOT NULL,
  used_at     TIMESTAMPTZ,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_email_tokens_user_id ON email_tokens(user_id);
CREATE UNIQUE INDEX idx_email_tokens_hash ON email_tokens(token_hash);

-- Down Migration

DROP TABLE email_tokens;
