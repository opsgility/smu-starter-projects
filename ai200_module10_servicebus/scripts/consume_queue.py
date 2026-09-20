"""Consume the shipment-events queue and DLQ any message with _force_failure=true."""
from __future__ import annotations

import logging
import sys

from lib.sb_consumer import receive_queue_loop

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def handle(payload: dict) -> None:
    if payload.get("_force_failure"):
        raise ValueError("poison message — DLQing on purpose")
    # Normal processing path:
    print(f"processed {payload['shipment_id']} description={payload['description']!r}")


def main() -> int:
    processed = receive_queue_loop(queue="shipment-events", handler=handle, max_loops=3)
    print(f"done — processed {processed} messages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
