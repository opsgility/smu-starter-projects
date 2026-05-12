"""Read latency probe — used to compare Strong vs Session consistency."""
from __future__ import annotations

import statistics
import time

from lib.cosmos_client import get_container


def main() -> None:
    container = get_container()
    latencies: list[float] = []
    for i in range(100):
        item_id = f"ship-{(i * 47) % 5000:06d}"
        t0 = time.perf_counter()
        try:
            container.read_item(item=item_id, partition_key="acme")
        except Exception:  # noqa: BLE001
            continue
        latencies.append((time.perf_counter() - t0) * 1000)
    if not latencies:
        print("no successful reads")
        return
    print(f"reads={len(latencies)}")
    print(f"  p50={statistics.median(latencies):.1f} ms")
    print(f"  p95={statistics.quantiles(latencies, n=20)[18]:.1f} ms")
    print(f"  max={max(latencies):.1f} ms")


if __name__ == "__main__":
    main()
