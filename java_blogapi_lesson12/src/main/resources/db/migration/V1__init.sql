-- TODO Exercise 1: Create the initial schema migration.
-- This replaces spring.jpa.hibernate.ddl-auto=create-drop with Flyway-managed schema.
-- Run the app and Flyway will execute this SQL automatically.

CREATE TABLE IF NOT EXISTS authors (
    id           BIGSERIAL PRIMARY KEY,
    username     VARCHAR(100) NOT NULL UNIQUE,
    email        VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    created_at   TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tags (
    id   BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS posts (
    id         BIGSERIAL PRIMARY KEY,
    title      VARCHAR(255) NOT NULL,
    content    TEXT,
    slug       VARCHAR(255),
    published  BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    version    BIGINT DEFAULT 0,
    author_id  BIGINT REFERENCES authors(id)
);

CREATE TABLE IF NOT EXISTS post_tags (
    post_id BIGINT REFERENCES posts(id),
    tag_id  BIGINT REFERENCES tags(id),
    PRIMARY KEY (post_id, tag_id)
);

CREATE TABLE IF NOT EXISTS comments (
    id         BIGSERIAL PRIMARY KEY,
    body       TEXT NOT NULL,
    created_at TIMESTAMP,
    post_id    BIGINT REFERENCES posts(id),
    author_id  BIGINT REFERENCES authors(id)
);
