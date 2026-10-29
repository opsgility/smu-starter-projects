-- Up Migration — intermediate "I know the password, now prove you have the second factor" state.

CREATE TABLE mfa_challenges (
  id          TEXT        PRIMARY KEY,
  user_id     INTEGER     NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  expires_at  TIMESTAMPTZ NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_mfa_challenges_user_id ON mfa_challenges(user_id);

-- Down Migration

DROP TABLE mfa_challenges;
