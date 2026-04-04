-- TODO Capstone Exercise 1: Add soft-delete column to comments
ALTER TABLE comments ADD COLUMN IF NOT EXISTS deleted BOOLEAN DEFAULT FALSE;
CREATE INDEX IF NOT EXISTS idx_comments_deleted ON comments(deleted);
