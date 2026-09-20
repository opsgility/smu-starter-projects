"""Drive concurrent /process requests at the LoadBalancer IP so HPA scales out."""
from __future__ import annotations

import argparse
import asyncio
import time

import httpx


async def hit(client: httpx.AsyncClient, url: str, idx: int) -> int:
    r = await client.post(
        f"{url}/process",
        json={"shipment_id": f"lg-{idx}", "description": "package soaked"},
        timeout=30,
    )
    return r.status_code


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--concurrency", type=int, default=40)
    ap.add_argument("--seconds", type=int, default=240)
    args = ap.parse_args()
    start = time.time()
    total = 0
    async with httpx.AsyncClient() as client:
        while time.time() - start < args.seconds:
            tasks = [hit(client, args.url, total + i) for i in range(args.concurrency)]
            for s in await asyncio.gather(*tasks, return_exceptions=True):
                if isinstance(s, int):
                    total += 1
            print(f"elapsed={int(time.time()-start)}s sent={total}")


if __name__ == "__main__":
    asyncio.run(main())
