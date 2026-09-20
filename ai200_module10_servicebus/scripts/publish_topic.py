"""Publish N events to the shipment-classifications topic.
Each message carries application properties used for subscription SQL filters."""
from __future__ import annotations

import argparse
import random
import sys

from lib.sb_producer import publish_topic_message

LABELS = ["water-damage", "crush-damage", "missing-item", "delayed", "temperature-excursion"]
TENANTS = ["acme", "contoso", "fabrikam"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default="shipment-classifications")
    ap.add_argument("--count", type=int, default=30)
    args = ap.parse_args()
    for i in range(args.count):
        label = random.choice(LABELS)
        tenant = random.choice(TENANTS)
        body = {
            "shipment_id": f"tp-{i:04d}",
            "label": label,
            "tenant": tenant,
        }
        publish_topic_message(
            args.topic,
            body,
            subject="classification",
            app_props={"label": label, "tenant": tenant},
        )
    print(f"published {args.count} events")
    return 0


if __name__ == "__main__":
    sys.exit(main())
