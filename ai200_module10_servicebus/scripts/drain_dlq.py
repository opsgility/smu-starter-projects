"""Drain and optionally resubmit dead-lettered messages."""
from __future__ import annotations

import argparse
import json
import logging
import sys

from lib.dlq_handler import drain_dlq

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", default="shipment-events")
    ap.add_argument("--resubmit", action="store_true")
    args = ap.parse_args()
    drained = drain_dlq(args.queue, resubmit=args.resubmit)
    print(f"drained {len(drained)} dead-lettered messages")
    print(json.dumps(drained, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
