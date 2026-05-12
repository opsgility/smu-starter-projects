"""Push N messages onto the Service Bus queue so KEDA scales the worker."""
from __future__ import annotations

import argparse
import json
import os

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage

DESCRIPTIONS = [
    "package soaked from rain",
    "crate crushed in transit",
    "item missing from shipment",
    "shipment delayed at port",
    "temperature excursion in cold chain",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=200)
    args = ap.parse_args()

    namespace = os.environ["SERVICEBUS_NAMESPACE"]
    queue = os.environ["SERVICEBUS_QUEUE"]
    cred = DefaultAzureCredential()
    with ServiceBusClient(fully_qualified_namespace=namespace, credential=cred) as client:
        with client.get_queue_sender(queue) as sender:
            for i in range(args.count):
                payload = {
                    "shipment_id": f"sb-{i:05d}",
                    "description": DESCRIPTIONS[i % len(DESCRIPTIONS)],
                }
                sender.send_messages(ServiceBusMessage(json.dumps(payload)))
                if (i + 1) % 50 == 0:
                    print(f"enqueued {i+1}/{args.count}")
    print(f"done — enqueued {args.count} messages")


if __name__ == "__main__":
    main()
