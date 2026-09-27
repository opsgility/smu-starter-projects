"""End-to-end smoke test — invoke all primitives directly."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from orion_mcp.server import (
    lookup_customer, apply_refund, escalate_to_csm,
    runbook, config, review_ticket, AUDIT,
)


def main():
    print("=== Tools ===")
    print("lookup acme-corp:", lookup_customer("acme-corp"))
    print("lookup widget-inc:", lookup_customer("widget-inc"))
    print("apply_refund acme $50:", apply_refund("acme-corp", 50, "goodwill"))
    print("apply_refund widget $50 (should fail):", apply_refund("widget-inc", 50, "goodwill"))
    print("escalate widget:", escalate_to_csm("widget-inc", "Suspended account refund request", "high"))
    print("\n=== Resources ===")
    print("runbook/sla:", runbook("sla"))
    print("config/current:", config())
    print("\n=== Prompts ===")
    print("review_ticket:", review_ticket("acme-corp export button broken since morning deploy"))
    print("\n=== AUDIT LOG ===")
    for a in AUDIT:
        print(" ", a)


if __name__ == "__main__":
    main()
