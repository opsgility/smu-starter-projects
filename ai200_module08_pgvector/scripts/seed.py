"""Seed 200 docs with embeddings + metadata. The doc text is a Northwind
shipment knowledge-base snippet; metadata.category is one of:
{"sop", "carrier-policy", "incident-template"}."""
from __future__ import annotations

import json
import sys
import uuid

from lib.embeddings import embed
from lib.rag import upsert_doc

DOCS = [
    ("acme", "sop",
     "When a package arrives soaked, photograph the outer box, log the carrier "
     "name, and file a wet-cargo claim within 24 hours."),
    ("acme", "sop",
     "Crush damage requires inner-content inspection before tendering the "
     "claim; missing items must be confirmed against the packing list."),
    ("acme", "carrier-policy",
     "DHL caps liability at $100 per kilo for ocean freight unless declared "
     "value was filed at pickup."),
    ("acme", "carrier-policy",
     "FedEx Priority Overnight cold-chain shipments must remain in the temp "
     "log range; excursions exceeding 30 minutes trigger automatic refunds."),
    ("acme", "incident-template",
     "Use form INC-WET when water intrusion is observed at delivery. Include "
     "humidity reading, photos, and carrier seal status."),
    ("contoso", "sop",
     "Temperature excursions on cold-chain shipments are logged at 5-minute "
     "intervals; if any reading exceeds 8C for over 30 minutes, escalate."),
    ("contoso", "carrier-policy",
     "UPS will refund cold-chain claims only if the temp logger reading is "
     "submitted within 72 hours of delivery."),
    ("contoso", "incident-template",
     "INC-TEMP requires the cold-chain log CSV, the carrier exception code, "
     "and a description of contents."),
    ("fabrikam", "sop",
     "Broken seal on a container is treated as a chain-of-custody event. "
     "Photograph seal number before opening."),
    ("fabrikam", "carrier-policy",
     "Maersk container seal breach incidents must be reported to the port "
     "authority within 4 hours."),
]


def main() -> int:
    inserted = 0
    for tenant, category, text in DOCS:
        for i in range(20):  # 10 * 20 = 200 docs
            doc_id = f"doc-{uuid.uuid4().hex[:12]}"
            full_text = text + (f" (variant {i})" if i else "")
            vec = embed(full_text)
            upsert_doc(
                doc_id=doc_id,
                tenant=tenant,
                text=full_text,
                embedding=vec,
                metadata={"category": category, "source": "seed", "variant": i},
            )
            inserted += 1
            if inserted % 50 == 0:
                print(f"inserted {inserted}")
    print(f"done — {inserted} docs inserted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
