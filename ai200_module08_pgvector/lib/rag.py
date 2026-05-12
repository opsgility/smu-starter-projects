"""Retrieval-augmented helpers backed by pgvector.

Student completes upsert_doc (Step 6a) and search_with_filter (Step 6b).
"""
from __future__ import annotations

from typing import Any

from lib.pg import get_conn


def upsert_doc(
    doc_id: str,
    tenant: str,
    text: str,
    embedding: list[float],
    metadata: dict[str, Any],
) -> None:
    """Insert or update one row in the docs table.

    TODO(step6a): replace this body. SQL template:

        INSERT INTO docs (id, tenant_id, text, embedding, metadata)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
          tenant_id = EXCLUDED.tenant_id,
          text      = EXCLUDED.text,
          embedding = EXCLUDED.embedding,
          metadata  = EXCLUDED.metadata;

    psycopg will accept `embedding` as a Python list[float] because
    register_vector() ran in get_conn(). Use psycopg.types.json.Jsonb(metadata).
    """
    raise NotImplementedError("Step 6a: implement upsert_doc — see TODO above")


def search_with_filter(
    query_embedding: list[float],
    tenant: str,
    category: str | None = None,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Return the top_k closest docs for `tenant`, optionally filtered by
    metadata->>'category' = category.

    TODO(step6b): replace this body. SQL template:

        SELECT id, text, metadata, embedding <=> %s AS distance
        FROM docs
        WHERE tenant_id = %s
          AND (%s IS NULL OR metadata->>'category' = %s)
        ORDER BY embedding <=> %s
        LIMIT %s;

    Note: <=> is cosine distance (lower = closer).
    """
    raise NotImplementedError("Step 6b: implement search_with_filter — see TODO above")
