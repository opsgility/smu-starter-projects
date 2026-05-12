"""Confirm get_client() returns a working CosmosClient. Run after Step 4."""
from __future__ import annotations

import os
import sys

from lib.cosmos_client import DATABASE_NAME, get_client


def main() -> int:
    client = get_client()
    endpoint = os.environ.get("COSMOS_ENDPOINT", "")
    print(f"[ok] connected to {endpoint}")
    # Force a real call (account read).
    info = client.get_database_account()
    print(f"[ok] account kind={info.ConsistencyPolicy.default_consistency_level} (or close)")
    # Try to access the database (will create it after Step 2 of the lab).
    try:
        db = client.get_database_client(DATABASE_NAME)
        db.read()
        print(f"[ok] database '{DATABASE_NAME}' exists")
    except Exception as exc:  # noqa: BLE001
        print(f"[note] database '{DATABASE_NAME}' not yet created: {exc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
