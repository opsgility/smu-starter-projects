-- Add auditing columns to posts table
ALTER TABLE posts ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS deleted BOOLEAN DEFAULT FALSE;
CREATE INDEX IF NOT EXISTS idx_posts_deleted ON posts(deleted);
