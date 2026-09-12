"""Insert 200 incident reports — these are the source documents the
change feed processor will pick up and embed."""
from __future__ import annotations

import sys
import uuid
from datetime import datetime, timezone

from lib.cosmos_client import INCIDENTS_CONTAINER, get_container

INCIDENTS = [
    ("acme",  "package soaked from heavy rain at the LAX dock"),
    ("acme",  "container ceiling leaked during transit from Hong Kong"),
    ("acme",  "outer carton crushed under stacked freight"),
    ("acme",  "shipment delayed 36 hours at the port of Long Beach"),
    ("acme",  "cold-chain temperature excursion of 8 degrees C for 4 hours"),
    ("acme",  "two items missing from the manifest at unboxing"),
    ("contoso","forklift puncture through pallet wrap"),
    ("contoso","frozen seafood thawed during customs hold"),
    ("contoso","shipment marked delivered but recipient denies receipt"),
    ("contoso","crate dented on left side, contents intact"),
    ("fabrikam","label illegible on arrival — scanner could not read"),
    ("fabrikam","driver reported broken seal on container 4Z9"),
    ("fabrikam","seal intact but inner box wet and moldy"),
    ("fabrikam","temperature sensor logged 4 hours above 8C"),
    ("fabrikam","tracker stopped reporting 50 km outside Frankfurt"),
]


def main() -> int:
    container = get_container(INCIDENTS_CONTAINER)
    inserted = 0
    for tenant, text in INCIDENTS:
        for i in range(14):  # 15 * 14 = 210 incidents
            doc = {
                "id": f"inc-{uuid.uuid4().hex[:12]}",
                "tenantId": tenant,
                "text": text + (f" (rep {i})" if i else ""),
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "metadata": {"source": "ops", "rep": i},
            }
            container.upsert_item(doc)
            inserted += 1
    print(f"inserted {inserted} incidents")
    return 0


if __name__ == "__main__":
    sys.exit(main())
