"""Subscribe to a single Service Bus topic subscription and log each message."""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("sub")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default="shipment-classifications")
    ap.add_argument("--sub", required=True, help="subscription name e.g. 'sub-water-damage'")
    ap.add_argument("--max-empty-loops", type=int, default=2)
    args = ap.parse_args()

    ns = os.environ["SERVICEBUS_NAMESPACE"]
    cred = DefaultAzureCredential()
    received = 0
    empty = 0
    with ServiceBusClient(fully_qualified_namespace=ns, credential=cred) as client:
        with client.get_subscription_receiver(args.topic, args.sub, max_wait_time=10) as recv:
            while empty < args.max_empty_loops:
                msgs = recv.receive_messages(max_message_count=20, max_wait_time=8)
                if not msgs:
                    empty += 1
                    continue
                empty = 0
                for m in msgs:
                    body = json.loads(b"".join(m.body))
                    log.info("sub=%s body=%s app_props=%s", args.sub, body, dict(m.application_properties or {}))
                    recv.complete_message(m)
                    received += 1
    print(f"done — received {received} on sub {args.sub}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
