"""Same query as query_slow.py — run AFTER applying the composite index
so you can compare the RU charge."""
from __future__ import annotations

from lib.cosmos_client import get_container

QUERY = (
    "SELECT TOP 50 c.id, c.status, c.createdAt FROM c "
    "WHERE c.tenantId=@tenant ORDER BY c.createdAt DESC"
)


def main() -> None:
    container = get_container()
    pager = container.query_items(
        query=QUERY,
        parameters=[{"name": "@tenant", "value": "acme"}],
        partition_key="acme",
        max_item_count=50,
    ).by_page()

    total_ru = 0.0
    total_items = 0
    for page in pager:
        items = list(page)
        ru = float(container.client_connection.last_response_headers.get("x-ms-request-charge", "0"))
        total_ru += ru
        total_items += len(items)
        print(f"page items={len(items)} RU={ru:.2f}")
        if not items:
            break
    print(f"\nTOTAL — items={total_items}  RU={total_ru:.2f}")


if __name__ == "__main__":
    main()
