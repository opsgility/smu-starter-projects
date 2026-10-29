-- Up Migration

ALTER TABLE users ADD COLUMN github_user_id BIGINT UNIQUE;

-- Down Migration

ALTER TABLE users DROP COLUMN github_user_id;
