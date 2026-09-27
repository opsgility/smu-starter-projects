"""Direct-invocation smoke test."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from server import review_ticket, escalate_alert, weekly_digest
    print("review_ticket:")
    print(f"  {review_ticket('The export button is broken since morning deploy.')[:120]}")
    print("\nescalate_alert (high):")
    print(f"  {escalate_alert('high', 'API down 15 minutes')[:120]}")
    print("\nweekly_digest:")
    msgs = weekly_digest("2026-09-22", 4)
    for m in msgs:
        print(f"  [{m.role}] {m.content[:80]}...")
except ImportError as e:
    print(f"TODO not filled: {e}")
