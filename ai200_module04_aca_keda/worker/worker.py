"""Service Bus queue consumer used by the second Container App in Module 4.

Reads messages from `SERVICEBUS_QUEUE` on `SERVICEBUS_NAMESPACE`, classifies
the description, then completes the message. KEDA's azure-servicebus scaler
watches the queue's active-message count and scales this app from 0 to N
replicas as work arrives.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import time

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusReceivedMessage

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("worker")


def classify(description: str) -> str:
    rules = [
        (("water", "soaked", "wet", "rain", "flood"), "water-damage"),
        (("crushed", "crush", "smashed", "broken", "dent"), "crush-damage"),
        (("missing", "lost", "stolen", "not found"), "missing-item"),
        (("late", "delayed", "delay", "stuck"), "delayed"),
        (("frozen", "thawed", "warm", "spoiled", "temperature"), "temperature-excursion"),
    ]
    t = description.lower()
    for keys, label in rules:
        if any(k in t for k in keys):
            return label
    return "unknown"


def main() -> int:
    namespace = os.environ["SERVICEBUS_NAMESPACE"]  # e.g. sb-ai200-xxxx.servicebus.windows.net
    queue = os.environ["SERVICEBUS_QUEUE"]          # e.g. shipments-in

    cred = DefaultAzureCredential()
    client = ServiceBusClient(fully_qualified_namespace=namespace, credential=cred)
    log.info("worker connected: namespace=%s queue=%s", namespace, queue)

    with client, client.get_queue_receiver(queue_name=queue, max_wait_time=30) as receiver:
        idle_loops = 0
        while True:
            msgs = receiver.receive_messages(max_message_count=10, max_wait_time=20)
            if not msgs:
                idle_loops += 1
                log.info("idle (%d)", idle_loops)
                if idle_loops >= 3:
                    # Let KEDA scale us back to zero.
                    return 0
                continue
            idle_loops = 0
            for m in msgs:
                handle(receiver, m)
    return 0


def handle(receiver, m: ServiceBusReceivedMessage) -> None:
    try:
        body = b"".join(m.body).decode("utf-8")
        payload = json.loads(body)
        label = classify(payload.get("description", ""))
        log.info(
            "processed shipment_id=%s label=%s seq=%s",
            payload.get("shipment_id"), label, m.sequence_number,
        )
        time.sleep(0.5)  # simulate inference latency
        receiver.complete_message(m)
    except Exception as exc:  # noqa: BLE001
        log.exception("failed: %s", exc)
        receiver.dead_letter_message(m, reason="processing-error", error_description=str(exc))


if __name__ == "__main__":
    sys.exit(main())
