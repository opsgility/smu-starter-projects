"""Bulk-insert 5000 fake shipments into the Cosmos DB shipments container."""
from __future__ import annotations

import json
import random
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from lib.cosmos_client import get_container

TENANTS = ["acme", "contoso", "fabrikam", "globex", "initech"]
STATUSES = ["in-transit", "delivered", "delayed", "returned", "lost"]
CARRIERS = ["ups", "fedex", "dhl", "usps", "ontrac"]


def shipment(i: int, base: datetime) -> dict:
    return {
        "id": f"ship-{i:06d}",
        "tenantId": random.choice(TENANTS),
        "status": random.choice(STATUSES),
        "carrier": random.choice(CARRIERS),
        "weight": round(random.uniform(0.5, 60.0), 2),
        "origin": random.choice(["LAX", "JFK", "ORD", "DFW", "SEA"]),
        "destination": random.choice(["MEX", "HKG", "LHR", "FRA", "NRT"]),
        "createdAt": (base + timedelta(seconds=i * 7)).isoformat(),
    }


def main() -> int:
    container = get_container()
    base = datetime.now(timezone.utc) - timedelta(days=30)

    target = 5000
    inserted = 0
    start = time.time()
    for i in range(target):
        container.upsert_item(shipment(i, base))
        inserted += 1
        if (i + 1) % 500 == 0:
            print(f"inserted {i+1}/{target}")
    elapsed = time.time() - start
    print(f"done — inserted {inserted} shipments in {elapsed:.1f}s ({inserted/elapsed:.0f}/s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
