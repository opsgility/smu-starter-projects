-- HNSW cosine index for fast approximate-NN. Build AFTER ingest for best perf
-- because pgvector's HNSW is faster to build over existing rows than to
-- maintain during many inserts.
CREATE INDEX IF NOT EXISTS docs_embedding_hnsw
ON docs USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
