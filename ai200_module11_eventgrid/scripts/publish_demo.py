"""Publish a mix of events to the custom topic."""
from __future__ import annotations

import argparse
import random
import sys

from lib.eg_publisher import publish_event

LABELS = ["water-damage", "crush-damage", "missing-item", "delayed"]
TENANTS = ["acme", "contoso", "fabrikam"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=20)
    args = ap.parse_args()
    for i in range(args.count):
        label = random.choice(LABELS)
        tenant = random.choice(TENANTS)
        publish_event(
            event_type="Northwind.Shipment.Classified",
            subject=f"shipments/{tenant}/sh-{i:04d}",
            data={
                "shipment_id": f"sh-{i:04d}",
                "tenant": tenant,
                "label": label,
                "confidence": round(random.uniform(0.6, 0.99), 2),
            },
        )
        if (i + 1) % 5 == 0:
            print(f"published {i+1}/{args.count}")
    print(f"done — published {args.count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
