"""Smoke test — invoke the resource functions directly."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from server import config, customer_profile, runbook
    print("config:", config())
    print("acme-corp profile:", customer_profile("acme-corp"))
    print("widget-inc profile:", customer_profile("widget-inc"))
    print("nonexistent profile:", customer_profile("nonexistent"))
    print("sla runbook:", runbook("sla"))
    print("refund runbook:", runbook("refund"))
except ImportError as e:
    print(f"TODO not filled: {e}")
