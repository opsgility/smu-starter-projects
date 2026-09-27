"""Exercise 4 — fire 20 tickets against all 3 versions and report cache metrics + $.

Runs each of 20 tickets against uncached / cached / cached_broken (60 calls
total, ~3-5 min wall clock). Reports for each version:
  - Total input tokens (uncached side)
  - Total cache_read_input_tokens (cache-hit tokens billed at ~10%)
  - Total cache_creation_input_tokens (cache-write tokens billed at ~125%)
  - Total output tokens
  - Total USD cost (at Sonnet 5 rates as of 2026-09-27)
  - Projected monthly cost at Orion's 200k tickets/month

Expected pattern:
  uncached       : ~$X — every call pays full input cost
  cached         : ~$X/10 (~90% savings) — first call writes cache, rest read
  cached_broken  : ~$X * 1.25 (~25% WORSE than uncached) — every call pays cache-write surcharge with zero read savings

Run: `python src/measure_caching.py`
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from classify_uncached import classify as cls_uncached  # noqa: E402
from classify_cached import classify as cls_cached  # noqa: E402
from classify_cached_broken import classify as cls_broken  # noqa: E402
from _shared import compute_cost_usd  # noqa: E402


TICKETS_PATH = Path(__file__).resolve().parent.parent / "data" / "tickets.json"
ORION_MONTHLY_TICKETS = 200_000


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    tickets = json.loads(TICKETS_PATH.read_text(encoding="utf-8"))
    print(f"measure_caching: {len(tickets)} tickets x 3 versions = {len(tickets)*3} calls "
          f"against model={model}\n")

    versions = [
        ("uncached", cls_uncached),
        ("cached", cls_cached),
        ("cached_broken", cls_broken),
    ]

    all_results: dict[str, list[dict]] = {name: [] for name, _ in versions}

    header = f"{'ID':<8} " + " ".join(
        f"{name[:16]:<32}" for name, _ in versions
    )
    subheader = f"{'':<8} " + " ".join(
        f"{'in/creat/read/out':<32}" for _ in versions
    )
    print(header)
    print(subheader)
    print("-" * len(header))

    for t in tickets:
        parts = [f"{t['id']:<8}"]
        for name, fn in versions:
            r = fn(client, model, t["text"])
            all_results[name].append(r)
            metrics = (f"{r['input_tokens']}/{r['cache_creation_input_tokens']}/"
                       f"{r['cache_read_input_tokens']}/{r['output_tokens']}")
            parts.append(f"{metrics[:31]:<32}")
        print(" ".join(parts))

    print("\nSummary — tokens + $ cost + monthly projection:")
    for name, _ in versions:
        rows = all_results[name]
        n = len(rows)
        total_in = sum(r["input_tokens"] for r in rows)
        total_create = sum(r["cache_creation_input_tokens"] for r in rows)
        total_read = sum(r["cache_read_input_tokens"] for r in rows)
        total_out = sum(r["output_tokens"] for r in rows)
        total_cost = sum(
            compute_cost_usd(
                r["input_tokens"], r["output_tokens"],
                r["cache_read_input_tokens"], r["cache_creation_input_tokens"],
            ) for r in rows
        )
        avg_cost = total_cost / n
        monthly_projection = avg_cost * ORION_MONTHLY_TICKETS
        print(f"  {name:<15}: "
              f"in={total_in:>6}  create={total_create:>6}  read={total_read:>6}  out={total_out:>4}   "
              f"total=${total_cost:.6f}   avg=${avg_cost:.6f}/call   "
              f"@{ORION_MONTHLY_TICKETS:,}/mo=${monthly_projection:,.2f}")

    print("\nInterpretation:")
    print("  - uncached      : the baseline. Every call pays full input token cost.")
    print("  - cached        : first call fills cache (creation surcharge); rest read at ~10% cost.")
    print("  - cached_broken : cache MISSES every call because timestamp above marker invalidates key.")
    print("                    Ends up MORE expensive than uncached due to the ~25% write surcharge.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
