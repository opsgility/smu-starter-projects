"""Drain the dead-letter queue, print each message, and optionally resubmit
to the main queue after fixing the payload."""
from __future__ import annotations

import json
import logging
import os
from typing import Iterable

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage

log = logging.getLogger("dlq")


def drain_dlq(queue: str, resubmit: bool = False) -> list[dict]:
    """Drain the dlq of `queue`. If resubmit=True, send a fixed copy back to the main queue.

    Pre-written for the lab — student calls this in Step 9.
    """
    ns = os.environ["SERVICEBUS_NAMESPACE"]
    cred = DefaultAzureCredential()
    drained = []
    with ServiceBusClient(fully_qualified_namespace=ns, credential=cred) as client:
        with client.get_queue_receiver(
            queue_name=queue,
            sub_queue="deadletter",
            max_wait_time=10,
        ) as dlq_recv:
            for m in dlq_recv:
                body_bytes = b"".join(m.body)
                try:
                    body = json.loads(body_bytes)
                except json.JSONDecodeError:
                    body = {"_raw": body_bytes.decode("utf-8", errors="replace")}
                info = {
                    "sequence_number": m.sequence_number,
                    "dead_letter_reason": m.dead_letter_reason,
                    "dead_letter_error_description": m.dead_letter_error_description,
                    "body": body,
                }
                drained.append(info)
                log.info("dlq message: %s", info)
                if resubmit:
                    fixed = dict(body)
                    fixed["_recovered_from_dlq"] = True
                    fixed.pop("_force_failure", None)  # remove the poison flag
                    with client.get_queue_sender(queue) as sender:
                        sender.send_messages(ServiceBusMessage(json.dumps(fixed)))
                dlq_recv.complete_message(m)
    return drained
