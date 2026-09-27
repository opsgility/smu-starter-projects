"""Exercise 4 — head-to-head across three reasoning strategies.

Runs 15 tickets against all three versions:
  1. escalate_no_reasoning (Sonnet 5 baseline)
  2. escalate_cot (Sonnet 5 + explicit <thinking>)
  3. escalate_adaptive (Opus 5.5 + output_config.effort:'high')

45 Claude calls, ~4-6 min wall clock. Reports accuracy, avg output
tokens, avg thinking tokens (adaptive only), and avg latency per version.

Run: `python src/measure_reasoning.py`
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from escalate_no_reasoning import decide as decide_none  # noqa: E402
from escalate_cot import decide as decide_cot, PROMPT_TEMPLATE as COT_PROMPT  # noqa: E402
from escalate_adaptive import decide as decide_adaptive, OUTPUT_CONFIG  # noqa: E402


TICKETS_PATH = Path(__file__).resolve().parent.parent / "data" / "escalation_tickets.json"


def _accuracy(rows: list[dict]) -> str:
    correct = sum(r["_correct"] for r in rows)
    n = len(rows)
    return f"{correct}/{n} ({100*correct/max(n,1):.0f}%)"


def _avg(rows: list[dict], key: str) -> float:
    vals = [r[key] for r in rows if r.get(key) is not None]
    return sum(vals) / max(len(vals), 1)


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    tickets = json.loads(TICKETS_PATH.read_text(encoding="utf-8"))
    print(f"measure_reasoning: {len(tickets)} tickets x 3 versions = {len(tickets)*3} calls\n")

    cot_ready = not COT_PROMPT.startswith("TODO")
    adaptive_ready = bool(OUTPUT_CONFIG)

    versions = [("no-reasoning", "sonnet-5", lambda t: decide_none(client, model, t), True)]
    versions.append(("cot", "sonnet-5", lambda t: decide_cot(client, model, t), cot_ready))
    versions.append(("adaptive", "opus-5-5", lambda t: decide_adaptive(client, t), adaptive_ready))

    all_results: dict[str, list[dict]] = {name: [] for name, _, _, _ in versions}

    header = f"{'ID':<7} {'expected':<12} " + " ".join(f"{name[:12]:<13}" for name, *_ in versions)
    print(header)
    print("-" * len(header))

    for t in tickets:
        parts = [f"{t['id']:<7}", f"{t['expected']:<12}"]
        for name, _tier, fn, ready in versions:
            if not ready:
                parts.append(f"{'(skip)':<13}")
                all_results[name].append({"_correct": False, "decision": None, "parse_ok": False,
                                          "input_tokens": 0, "output_tokens": 0, "thinking_tokens": 0,
                                          "latency_ms": 0})
                continue
            r = fn(t["text"])
            correct = (r.get("decision") or "").lower() == t["expected"].lower()
            r["_correct"] = correct
            all_results[name].append(r)
            parts.append(f"{('✓' if correct else '✗') + ' ' + (r.get('decision') or 'FAIL')[:10]:<13}")
        print(" ".join(parts))

    print("\nSummary — accuracy + cost + latency:")
    for name, tier, _fn, ready in versions:
        rows = all_results[name]
        if not ready:
            print(f"  {name:<14} [{tier:<8}]: (skipped — module TODO not filled in)")
            continue
        acc = _accuracy(rows)
        avg_out = _avg(rows, "output_tokens")
        avg_think = _avg(rows, "thinking_tokens")
        avg_lat = _avg(rows, "latency_ms")
        think_str = f" +thinking={avg_think:.0f}" if avg_think > 0 else ""
        print(f"  {name:<14} [{tier:<8}]: accuracy={acc}  avg_output_tokens={avg_out:.0f}{think_str}  "
              f"avg_latency_ms={avg_lat:.0f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
