-- TODO Exercise 2: Add a seed data migration.
INSERT INTO authors (username, email, display_name, created_at) VALUES
    ('admin', 'admin@blog.com', 'Admin User', NOW()),
    ('alice', 'alice@blog.com', 'Alice Writer', NOW())
ON CONFLICT (username) DO NOTHING;

INSERT INTO tags (name) VALUES ('java'), ('spring-boot'), ('tutorial')
ON CONFLICT (name) DO NOTHING;
