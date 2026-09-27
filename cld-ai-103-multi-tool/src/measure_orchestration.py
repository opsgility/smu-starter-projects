"""Exercise 4 — measure iteration count + tool_call pattern + latency across scenarios.

Runs 5 scenarios against BOTH agent_sequential and agent_parallel, reports
iterations, tool_calls, and wall-clock time. Also asserts expected tool-call
sequences per scenario.

Run: `python src/measure_orchestration.py`
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent_sequential import run_agent as run_seq
from agent_parallel import run_agent as run_par
from tools import AUDIT_LOG


SCENARIOS = [
    {"id": "S1-enterprise-refund",
     "prompt": "Customer 'acme-corp' wants a $200 goodwill credit for last week's API 502 outage. Handle it.",
     "expected_tools_used": ["get_customer_status", "search_recent_tickets", "apply_refund"]},
    {"id": "S2-suspended-refund",
     "prompt": "Customer 'widget-inc' asked for a refund. Handle it.",
     "expected_tools_used": ["get_customer_status", "escalate_to_human"]},
    {"id": "S3-pro-outage-pattern",
     "prompt": "Customer 'beta-labs' has been having recurring issues all week. Look at their state and recent tickets and recommend an action.",
     "expected_tools_used": ["get_customer_status", "search_recent_tickets", "escalate_to_human"]},
    {"id": "S4-cancelled-reactivation",
     "prompt": "Customer 'quantum-data' emailed asking about reactivation. Handle it.",
     "expected_tools_used": ["get_customer_status", "escalate_to_human"]},
    {"id": "S5-enterprise-small-issue",
     "prompt": "Customer 'orbit-metrics' has one open incident about a stale report. Look them up and decide next steps.",
     "expected_tools_used": ["get_customer_status", "search_recent_tickets"]},
]


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    print(f"measure_orchestration: {len(SCENARIOS)} scenarios x 2 agents against model={model}\n")
    print(f"{'ID':<26} {'seq iters':<11} {'seq tools':<22} {'par iters':<11} {'par tools':<22}")
    print("-" * 92)

    for s in SCENARIOS:
        AUDIT_LOG.clear()
        try:
            t0 = time.perf_counter(); seq = run_seq(client, model, s["prompt"]); seq_ms = int((time.perf_counter()-t0)*1000)
        except Exception as e:
            print(f"{s['id']:<26}  seq FAILED: {e}"); continue
        seq_tool_names = [name for name, _ in seq["tool_calls"]]

        AUDIT_LOG.clear()
        try:
            t0 = time.perf_counter(); par = run_par(client, model, s["prompt"]); par_ms = int((time.perf_counter()-t0)*1000)
        except Exception as e:
            print(f"{s['id']:<26}  par FAILED: {e}"); continue
        par_tool_names = [name for name, _ in par["tool_calls"]]

        seq_summary = ",".join(n[:3] for n in seq_tool_names)
        par_summary = ",".join(n[:3] for n in par_tool_names)
        print(f"{s['id']:<26} {seq['iterations']:<11} {seq_summary[:20]:<22} "
              f"{par['iterations']:<11} {par_summary[:20]:<22}")

        # Assertion: expected tools were used (order-agnostic, subset OK)
        expected_set = set(s["expected_tools_used"])
        seq_ok = expected_set.issubset(set(seq_tool_names))
        par_ok = expected_set.issubset(set(par_tool_names))
        print(f"  expected: {sorted(expected_set)}  seq_ok={seq_ok}  par_ok={par_ok}")
        print(f"  seq_total_ms={seq_ms}  par_total_ms={par_ms}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
