"""Change feed processor that watches `incidents` and writes embeddings
to `incident_vectors`. Used by scripts/changefeed_processor.py.

The student completes the on_new_incident() TODO in Step 8.
"""
from __future__ import annotations

import logging
from typing import Iterable

from lib.cosmos_client import INCIDENTS_CONTAINER, INCIDENT_VECTORS_CONTAINER, get_container
from lib.embeddings import embed
from lib.vector_store import upsert_vector

log = logging.getLogger("changefeed")


def on_new_incident(item: dict) -> None:
    """Called once per new/changed incident document. Embed its text and
    upsert into incident_vectors.

    TODO(step8): replace this body. The function should:
      1. Pull item["id"], item["tenantId"], item["text"]
      2. Compute embedding = embed(text)
      3. Call upsert_vector(item_id, tenant, text, embedding, metadata=item.get("metadata"))
    """
    raise NotImplementedError("Step 8: implement on_new_incident — see TODO above")


def run_once(continuation: str | None = None) -> str | None:
    """Read the change feed once from `continuation` (or beginning).

    Returns the next continuation token to persist between runs.
    """
    container = get_container(INCIDENTS_CONTAINER)
    response = container.query_items_change_feed(
        is_start_from_beginning=continuation is None,
        continuation=continuation,
    )
    count = 0
    for item in response:
        on_new_incident(item)
        count += 1
    new_continuation = container.client_connection.last_response_headers.get("etag", "")
    log.info("processed %d items, new continuation=%s", count, new_continuation[:20])
    return new_continuation or None
