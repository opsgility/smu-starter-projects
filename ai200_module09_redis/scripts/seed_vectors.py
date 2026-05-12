"""Seed the RediSearch HNSW index with 100 docs."""
from __future__ import annotations

import sys
import uuid

from lib.embeddings import embed
from lib.vector_index import create_index, upsert_doc

DOCS = [
    ("acme", "sop", "Wet cargo claims must be filed within 24 hours of delivery."),
    ("acme", "sop", "Crush damage requires inner-content inspection before claim."),
    ("acme", "policy", "DHL caps liability at $100 per kilo for ocean freight."),
    ("acme", "policy", "Declared value must be filed at pickup to override default caps."),
    ("contoso", "sop", "Cold-chain excursions over 30 minutes require escalation."),
    ("contoso", "policy", "UPS refunds cold-chain claims only with 72h logger submission."),
    ("fabrikam", "sop", "Broken seal is a chain-of-custody event — photograph first."),
    ("fabrikam", "policy", "Maersk seal breach must be reported within 4 hours."),
]


def main() -> int:
    create_index()
    inserted = 0
    for tenant, category, text in DOCS:
        for i in range(13):  # 8 * 13 = 104 docs
            doc_id = f"doc-{uuid.uuid4().hex[:10]}"
            v = embed(text + (f" (rev {i})" if i else ""))
            upsert_doc(doc_id=doc_id, tenant=tenant, category=category,
                       text=text + (f" (rev {i})" if i else ""),
                       embedding=v)
            inserted += 1
            if inserted % 25 == 0:
                print(f"inserted {inserted}")
    print(f"done — {inserted} docs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
