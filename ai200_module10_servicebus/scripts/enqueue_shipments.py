"""Push N test messages onto the shipments queue (used to exercise the SB trigger)."""
from __future__ import annotations

import argparse
import json
import os

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=10)
    args = ap.parse_args()

    ns = os.environ["SERVICEBUS_NAMESPACE"]
    cred = DefaultAzureCredential()
    with ServiceBusClient(fully_qualified_namespace=ns, credential=cred) as client:
        with client.get_queue_sender("shipments") as sender:
            for i in range(args.count):
                body = {
                    "shipment_id": f"fn-{i:04d}",
                    "description": "package soaked from rain on the dock" if i % 2 == 0 else "crate crushed in transit",
                }
                sender.send_messages(ServiceBusMessage(json.dumps(body)))
    print(f"queued {args.count} shipments")


if __name__ == "__main__":
    main()
