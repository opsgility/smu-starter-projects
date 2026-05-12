"""Seed the incident_vectors container with 100 Northwind FAQs (for the RAG layer)."""
from __future__ import annotations

import sys
import uuid

from lib.cosmos_vector import container
from lib.embeddings import embed

FAQS = [
    ("acme", "How long do I have to file a wet-cargo claim? Within 24 hours of delivery."),
    ("acme", "Photograph the outer box, log carrier, and file the wet-cargo claim form."),
    ("acme", "Crush damage requires inner-content inspection before tendering the claim."),
    ("acme", "DHL caps liability at $100 per kilo for ocean freight."),
    ("acme", "Declared value must be filed at pickup to override the default cap."),
    ("contoso", "Temperature excursions over 30 minutes require escalation to the carrier."),
    ("contoso", "UPS refunds cold-chain claims only when the logger reading is submitted within 72 hours."),
    ("contoso", "Submit Form INC-TEMP plus the cold-chain log CSV for any temperature event."),
    ("fabrikam", "Broken seal is a chain-of-custody event — photograph seal before opening."),
    ("fabrikam", "Maersk container seal breach must be reported to port authority within 4 hours."),
]


def main() -> int:
    c = container()
    inserted = 0
    for tenant, text in FAQS:
        for i in range(10):
            text_full = text + (f" (variant {i})" if i else "")
            vec = embed(text_full)
            c.upsert_item({
                "id": f"faq-{uuid.uuid4().hex[:12]}",
                "tenantId": tenant,
                "text": text_full,
                "embedding": vec,
                "metadata": {"source": "capstone-seed"},
            })
            inserted += 1
            if inserted % 25 == 0:
                print(f"inserted {inserted}")
    print(f"done — {inserted} FAQs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
