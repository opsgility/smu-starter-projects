"""Service Bus producer — sends queue messages and topic messages.

Student fills in the TODOs in Step 5.
"""
from __future__ import annotations

import json
import os
from typing import Any

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def _client() -> ServiceBusClient:
    return ServiceBusClient(
        fully_qualified_namespace=os.environ["SERVICEBUS_NAMESPACE"],
        credential=DefaultAzureCredential(),
    )


def send_queue_message(queue: str, body: dict[str, Any], subject: str | None = None) -> None:
    """Send one message to a queue.

    TODO(step5a): replace this body. Use _client() and client.get_queue_sender(queue).
    Build ServiceBusMessage(body=json.dumps(body), subject=subject).
    """
    raise NotImplementedError("Step 5a: implement send_queue_message")


def publish_topic_message(topic: str, body: dict[str, Any], subject: str | None = None, app_props: dict[str, Any] | None = None) -> None:
    """Publish one message to a topic with optional application properties
    (used for subscription SQL filters).

    TODO(step5b): replace this body. ServiceBusMessage(...) accepts an
    `application_properties` kwarg.
    """
    raise NotImplementedError("Step 5b: implement publish_topic_message")
