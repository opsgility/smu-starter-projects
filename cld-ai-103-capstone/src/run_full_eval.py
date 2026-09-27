"""Exercise 4 — run the production_agent against 15 eval cases + score."""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from production_agent import run_production_agent
from eval_harness import score_case
from tools import AUDIT_LOG


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    cases_path = Path(__file__).resolve().parent.parent / "data" / "eval_cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))

    print(f"run_full_eval: {len(cases)} cases against model={model}\n")

    pass_count = 0
    kind_counts: dict[str, dict[str, int]] = {}

    for c in cases:
        AUDIT_LOG.clear()
        print(f"\n{'='*70}\n[{c['id']} kind={c['kind']}] {c['prompt']}\n{'='*70}")

        try:
            result = run_production_agent(client, model, c["prompt"], max_iterations=15)
        except NotImplementedError as e:
            print(f"  production_agent TODO not filled: {e}")
            continue
        except Exception as e:
            print(f"  AGENT CRASHED: {type(e).__name__}: {e}")
            continue

        try:
            scored = score_case(client, model, result, c["expected"])
        except Exception as e:
            print(f"  SCORING CRASHED: {type(e).__name__}: {e}")
            continue

        print(f"  tools_used: {result['tools_used']}")
        print(f"  action: {(result.get('action_record') or {}).get('decided_action')}")
        for chk in scored["deterministic"]["checks"]:
            print(f"    {'✓' if chk['passed'] else '✗'} {chk['name']}" + (f" (got={chk.get('got')})" if 'got' in chk else ''))
        for sem in scored["semantic"]:
            print(f"    {'✓' if sem['passed'] else '✗'} [judge] {sem['criterion'][:60]}")
        print(f"  RESULT: {'✓ PASS' if scored['all_passed'] else '✗ FAIL'}")

        if scored["all_passed"]:
            pass_count += 1
        kd = kind_counts.setdefault(c["kind"], {"pass": 0, "total": 0})
        kd["total"] += 1
        if scored["all_passed"]:
            kd["pass"] += 1

    print(f"\n{'='*70}\nSummary: {pass_count}/{len(cases)} cases passed")
    for kind, kd in sorted(kind_counts.items()):
        print(f"  {kind:<12}: {kd['pass']}/{kd['total']} ({100*kd['pass']/max(kd['total'],1):.0f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
