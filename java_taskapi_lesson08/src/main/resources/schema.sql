-- Run this script to create the tasks table in your PostgreSQL database
-- psql -U postgres -d taskdb -f schema.sql

CREATE TABLE IF NOT EXISTS tasks (
    id          BIGSERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    status      VARCHAR(50)  NOT NULL DEFAULT 'PENDING',
    due_date    VARCHAR(20)
);
