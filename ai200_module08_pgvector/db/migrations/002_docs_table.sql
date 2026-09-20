CREATE TABLE IF NOT EXISTS docs (
    id          TEXT PRIMARY KEY,
    tenant_id   TEXT NOT NULL,
    text        TEXT NOT NULL,
    embedding   vector(1536) NOT NULL,
    metadata    JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS docs_tenant_idx ON docs (tenant_id);
CREATE INDEX IF NOT EXISTS docs_metadata_gin ON docs USING GIN (metadata);
