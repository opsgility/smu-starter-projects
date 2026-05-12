"""Drive enough concurrent requests at the FastAPI app to force KEDA
to scale out replicas. Used in Step 6 of the lab."""
from __future__ import annotations

import argparse
import asyncio
import time

import httpx


async def hit(client: httpx.AsyncClient, url: str, idx: int) -> int:
    body = {
        "shipment_id": f"loadgen-{idx}",
        "description": "package soaked from rain on the dock",
    }
    r = await client.post(f"{url}/process", json=body, timeout=30)
    return r.status_code


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Container App FQDN, e.g. https://classifier.<id>.<region>.azurecontainerapps.io")
    ap.add_argument("--concurrency", type=int, default=30)
    ap.add_argument("--seconds", type=int, default=120)
    args = ap.parse_args()

    start = time.time()
    total = 0
    seen_replicas: set[str] = set()
    async with httpx.AsyncClient() as client:
        while time.time() - start < args.seconds:
            tasks = [hit(client, args.url, total + i) for i in range(args.concurrency)]
            for s in await asyncio.gather(*tasks, return_exceptions=True):
                if isinstance(s, int):
                    total += 1
            # Sample one to track replica count
            r = await client.get(f"{args.url}/healthz")
            if r.status_code == 200:
                seen_replicas.add(r.json().get("replica", "?"))
            print(f"elapsed={int(time.time()-start)}s sent={total} replicas_seen={len(seen_replicas)}")
    print(f"\nFinal: sent={total} unique_replicas={len(seen_replicas)}")
    for r in sorted(seen_replicas):
        print(f"  - {r}")


if __name__ == "__main__":
    asyncio.run(main())
