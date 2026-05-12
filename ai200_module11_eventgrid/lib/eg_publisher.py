"""Event Grid publisher for the custom topic.

Student completes the publish_event TODO in Step 5.
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.eventgrid import EventGridPublisherClient, EventGridEvent


def _client() -> EventGridPublisherClient:
    endpoint = os.environ["EG_TOPIC_ENDPOINT"]
    key = os.environ["EG_TOPIC_KEY"]
    return EventGridPublisherClient(endpoint, AzureKeyCredential(key))


def publish_event(
    event_type: str,
    subject: str,
    data: dict[str, Any],
    data_version: str = "1.0",
) -> None:
    """Publish one custom event.

    TODO(step5): replace this body. Construct an EventGridEvent with:
      - id = uuid4 hex
      - event_type = event_type
      - subject = subject
      - data = data
      - event_time = datetime.now(timezone.utc)
      - data_version = data_version
    Then call _client().send([event]).
    """
    raise NotImplementedError("Step 5: implement publish_event")
