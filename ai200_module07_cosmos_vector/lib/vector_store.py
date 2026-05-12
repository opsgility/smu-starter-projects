"""Vector search helper. The student completes the TODOs in Step 6.

The completed module performs:
  - upsert_vector(item_id, tenant, text, embedding, metadata) into incident_vectors
  - search_similar(query_embedding, top_k, tenant) using VectorDistance()
"""
from __future__ import annotations

import os
from typing import Any

from azure.cosmos import ContainerProxy

from lib.cosmos_client import INCIDENT_VECTORS_CONTAINER, get_container


def upsert_vector(
    item_id: str,
    tenant: str,
    text: str,
    embedding: list[float],
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Upsert one item into the incident_vectors container.

    TODO(step6a): replace this body. The container's partition key is /tenantId,
    so the item must include "id", "tenantId", "text", "embedding", and optionally "metadata".
    Use container.upsert_item(item=...) and return the result.
    """
    raise NotImplementedError("Step 6a: implement upsert_vector — see TODO above")


def search_similar(
    query_embedding: list[float],
    top_k: int = 5,
    tenant: str | None = None,
) -> list[dict[str, Any]]:
    """Find top_k most-similar items using VectorDistance.

    TODO(step6b): replace this body. The query should be of the form:

        SELECT TOP @k c.id, c.text, c.metadata,
                      VectorDistance(c.embedding, @q) AS score
        FROM c
        WHERE c.tenantId = @tenant   -- only if tenant is not None
        ORDER BY VectorDistance(c.embedding, @q)

    Use enable_cross_partition_query=True when tenant is None.
    """
    raise NotImplementedError("Step 6b: implement search_similar — see TODO above")
