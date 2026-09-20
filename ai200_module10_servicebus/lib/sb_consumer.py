"""Service Bus consumer — queue receiver with retry + DLQ on poison messages.

The student completes the TODO in Step 7.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Callable

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusReceivedMessage

log = logging.getLogger("consumer")


def receive_queue_loop(
    queue: str,
    handler: Callable[[dict], None],
    *,
    max_loops: int = 5,
    max_wait_time: int = 10,
    max_message_count: int = 10,
) -> int:
    """Receive and process messages from `queue`. On exception, DLQ the
    message with a reason.

    TODO(step7): replace this body. For each message:
      1. Parse body bytes -> JSON dict
      2. Call handler(payload)
      3. On success: receiver.complete_message(m)
      4. On exception: receiver.dead_letter_message(m, reason="...", error_description=str(exc))

    Loop until `max_loops` of consecutive empty receives, then return total processed.
    """
    raise NotImplementedError("Step 7: implement receive_queue_loop")
