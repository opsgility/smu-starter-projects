"""Exercise 3 — stress-test the robust agent under 4 failure scenarios."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from safe_agent import run_agent
from flaky_tools import CALL_LOG


SCENARIOS = [
    {"id": "R1-flaky-40pct",
     "env": {"FLAKY_PROB": "0.4"},
     "prompt": "Customer 'acme-corp' wants a $150 refund for last week's incident. Handle it.",
     "expect": "should succeed despite retries (retries recover 40% flakes)"},
    {"id": "R2-flaky-heavy",
     "env": {"FLAKY_PROB": "0.7"},
     "prompt": "Customer 'beta-labs' opened a support ticket about ingest pipeline. Look them up and recommend action.",
     "expect": "should mostly succeed but some tool calls may exhaust retries"},
    {"id": "R3-permanent-fail-tool",
     "env": {"FLAKY_PROB": "0.0", "PERMANENT_FAIL_TOOL": "apply_refund"},
     "prompt": "Customer 'acme-corp' wants a $100 refund. Handle it.",
     "expect": "apply_refund always 400s → agent should escalate instead"},
    {"id": "R4-clean-baseline",
     "env": {"FLAKY_PROB": "0.0"},
     "prompt": "Customer 'widget-inc' asked for a refund.",
     "expect": "no failure injection; agent should escalate (widget-inc suspended)"},
]


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    print(f"test_robustness: {len(SCENARIOS)} scenarios against model={model}\n")

    for s in SCENARIOS:
        # Set failure-injection env vars for this scenario
        for k, v in s["env"].items():
            os.environ[k] = v
        # Clear vars we're not setting (avoid bleed between scenarios)
        for k in ("FLAKY_PROB", "PERMANENT_FAIL_TOOL"):
            if k not in s["env"]:
                os.environ.pop(k, None)

        CALL_LOG.clear()
        print(f"\n{'='*70}\n[{s['id']}] {s['expect']}\n{'='*70}")

        try:
            result = run_agent(client, model, s["prompt"], max_iterations=15, max_tool_calls=40)
            print(f"iterations={result['iterations']}  tool_call_count={result['tool_call_count']}  "
                  f"circuit={result['circuit_tripped']}")
            print(f"final: {result['final_text'][:400]}...")
            print(f"call_log_length={len(CALL_LOG)}  (includes retries)")
        except Exception as e:
            print(f"AGENT CRASHED: {type(e).__name__}: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
