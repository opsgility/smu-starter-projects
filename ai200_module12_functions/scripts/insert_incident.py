"""Insert one incident into Cosmos `incidents` so the change feed fires."""
from __future__ import annotations

import json
import os
import uuid

from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential


def main() -> None:
    endpoint = os.environ["COSMOS_ENDPOINT"]
    key = os.environ.get("COSMOS_KEY")
    client = CosmosClient(endpoint, credential=key) if key else CosmosClient(endpoint, credential=DefaultAzureCredential())
    c = client.get_database_client("northwind").get_container_client("incidents")
    doc = {
        "id": f"inc-{uuid.uuid4().hex[:12]}",
        "tenantId": "acme",
        "text": "package soaked from rain",
    }
    c.upsert_item(doc)
    print(f"inserted {doc['id']}")


if __name__ == "__main__":
    main()
