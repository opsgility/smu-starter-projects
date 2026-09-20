"""Service Bus producer used by the API to fan-out classification work."""
from __future__ import annotations

import json
import os
from typing import Any

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def send_to_queue(queue: str, body: dict[str, Any]) -> None:
    ns = os.environ["SERVICEBUS_NAMESPACE"]
    with ServiceBusClient(fully_qualified_namespace=ns, credential=DefaultAzureCredential()) as client:
        with client.get_queue_sender(queue) as sender:
            sender.send_messages(ServiceBusMessage(json.dumps(body)))
