-- V2__create_notification_log.sql
CREATE TABLE notification_log (
    id            BIGSERIAL PRIMARY KEY,
    customer_id   BIGINT NOT NULL,
    email         VARCHAR(255) NOT NULL,
    processed_at  TIMESTAMPTZ DEFAULT NOW(),
    status        VARCHAR(50) NOT NULL
);
