"""RediSearch HNSW vector index. The student completes the TODOs in Step 8."""
from __future__ import annotations

import struct
from typing import Any

import numpy as np
from redis.commands.search.field import VectorField, TextField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

from lib.redis_client import get_redis

INDEX_NAME = "idx:docs"
KEY_PREFIX = "doc:"
VECTOR_DIM = 1536


def to_bytes(embedding: list[float]) -> bytes:
    return np.asarray(embedding, dtype=np.float32).tobytes()


def create_index() -> None:
    """Create the RediSearch HNSW cosine index. Idempotent."""
    r = get_redis()
    try:
        r.ft(INDEX_NAME).info()
        return  # already exists
    except Exception:  # noqa: BLE001
        pass

    schema = (
        TextField("text"),
        TagField("tenant"),
        TagField("category"),
        VectorField(
            "embedding",
            "HNSW",
            {"TYPE": "FLOAT32", "DIM": VECTOR_DIM, "DISTANCE_METRIC": "COSINE", "M": 16, "EF_CONSTRUCTION": 64},
        ),
    )
    definition = IndexDefinition(prefix=[KEY_PREFIX], index_type=IndexType.HASH)
    r.ft(INDEX_NAME).create_index(fields=schema, definition=definition)


def upsert_doc(doc_id: str, tenant: str, category: str, text: str, embedding: list[float]) -> None:
    """Write one document as a Redis hash.

    TODO(step8a): replace this body. Use r.hset(key, mapping=...) where:
      - key = f"{KEY_PREFIX}{doc_id}"
      - "text": text.encode()
      - "tenant": tenant.encode()
      - "category": category.encode()
      - "embedding": to_bytes(embedding)
    """
    raise NotImplementedError("Step 8a: implement upsert_doc — see TODO above")


def knn_search(query_embedding: list[float], top_k: int = 5, tenant: str | None = None) -> list[dict[str, Any]]:
    """Vector KNN search with optional tenant filter.

    TODO(step8b): replace this body. Construct a Query like:
        f"(@tenant:{{{tenant}}})=>[KNN {top_k} @embedding $vec AS score]"
    or  f"*=>[KNN {top_k} @embedding $vec AS score]" if tenant is None.
    Set query_params={"vec": to_bytes(query_embedding)}, sort_by("score"),
    return_fields("text", "tenant", "category", "score"), and dialect=2.

    Run r.ft(INDEX_NAME).search(query). Convert results to a list of dicts.
    """
    raise NotImplementedError("Step 8b: implement knn_search — see TODO above")
