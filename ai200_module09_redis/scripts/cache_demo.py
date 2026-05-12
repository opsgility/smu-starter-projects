"""Demonstrates the cache-aside wrapper. Run twice — the second call hits."""
from __future__ import annotations

import sys
import time

from lib.cache import cached_call
from lib.embeddings import chat


def main() -> int:
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Summarize Northwind wet-cargo policy in one sentence."
    for i in range(2):
        t0 = time.perf_counter()
        text, hit = cached_call(prompt, chat, ttl_seconds=600)
        dt = (time.perf_counter() - t0) * 1000
        print(f"call {i+1}: hit={hit}  latency={dt:.0f}ms")
        print(f"  -> {text[:120]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
