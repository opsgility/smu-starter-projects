"""Send N messages to the shipment-events queue.
Use --poison to flip one in five into an intentionally-poisoned payload."""
from __future__ import annotations

import argparse
import sys

from lib.sb_producer import send_queue_message


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", default="shipment-events")
    ap.add_argument("--count", type=int, default=20)
    ap.add_argument("--poison", action="store_true",
                    help="Mark every fifth message with _force_failure=true to exercise DLQ")
    args = ap.parse_args()
    for i in range(args.count):
        body = {
            "shipment_id": f"sb-{i:04d}",
            "description": "package soaked from rain",
            "weight_kg": (i + 1) * 1.5,
        }
        if args.poison and i % 5 == 0:
            body["_force_failure"] = True
        send_queue_message(args.queue, body, subject=f"event-{i}")
    print(f"sent {args.count} messages to {args.queue} (poison={args.poison})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
