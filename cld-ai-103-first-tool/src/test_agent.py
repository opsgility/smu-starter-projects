"""Exercise 3 — smoke-test the agent against 4 scenarios.

Runs the agent with 4 different prompts covering:
  1. Suspended account refund — agent should NOT recommend refund.
  2. Active enterprise customer — agent should recommend refund + confirmation.
  3. Cancelled customer requesting reactivation info — agent explains next steps.
  4. Unknown customer — agent handles the error result gracefully.

Prints each scenario's final answer + a pass/fail summary based on
substring-match assertions.

Run: `python src/test_agent.py`
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent import run_agent


SCENARIOS = [
    {
        "id": "S1-suspended",
        "prompt": "Customer 'widget-inc' opened a ticket asking for a refund on their last invoice. Should we process it?",
        "expected_substrings": ["suspend", "widget-inc"],
        "expected_refund_recommendation": False,
    },
    {
        "id": "S2-enterprise",
        "prompt": "Customer 'acme-corp' requested a goodwill credit for the outage last week. What should we do?",
        "expected_substrings": ["acme-corp", "enterprise"],
        "expected_refund_recommendation": True,
    },
    {
        "id": "S3-cancelled",
        "prompt": "Customer 'quantum-data' wants to know how to reactivate their account. Give them next steps.",
        "expected_substrings": ["quantum-data", "cancel"],
        "expected_refund_recommendation": False,
    },
    {
        "id": "S4-unknown",
        "prompt": "Customer 'nonexistent-corp' opened a ticket. Look them up and tell me their status.",
        "expected_substrings": ["not found", "nonexistent-corp"],
        "expected_refund_recommendation": False,
    },
]


def _refund_recommended(text: str) -> bool:
    lo = text.lower()
    # Positive signals for recommending a refund/credit.
    positive = any(kw in lo for kw in ["process the refund", "issue the credit",
                                        "approve the refund", "provide the credit",
                                        "goodwill credit", "process a credit"])
    # Negative signals.
    negative = any(kw in lo for kw in ["cannot process", "do not process",
                                        "should not refund", "not eligible for a refund",
                                        "decline the refund"])
    return positive and not negative


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    print(f"test_agent: 4 scenarios against model={model}\n")

    passed = 0
    failed = 0

    for s in SCENARIOS:
        print(f"\n{'='*70}")
        print(f"[{s['id']}] {s['prompt']}")
        print(f"{'='*70}")

        try:
            final = run_agent(client, model, s["prompt"], verbose=False)
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
            continue

        print(f"final answer:\n{final}\n")

        # Assertions
        checks = []
        for sub in s["expected_substrings"]:
            ok = sub.lower() in final.lower()
            checks.append((f"contains '{sub}'", ok))

        refund_actual = _refund_recommended(final)
        checks.append((f"refund_recommended={s['expected_refund_recommendation']} (got {refund_actual})",
                       refund_actual == s["expected_refund_recommendation"]))

        all_ok = all(ok for _, ok in checks)
        for desc, ok in checks:
            print(f"  {'✓' if ok else '✗'} {desc}")
        if all_ok:
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*70}")
    print(f"Summary: {passed} passed / {failed} failed / {len(SCENARIOS)} total")
    print(f"{'='*70}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
