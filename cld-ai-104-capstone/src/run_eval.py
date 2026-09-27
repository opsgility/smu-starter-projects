"""Exercise 3 — full 4-dimension RAG eval scorecard."""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline import ask
from faithfulness_judge import judge_faithfulness


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    cases = json.loads((Path(__file__).resolve().parent.parent / "data" / "eval_cases.json").read_text())
    print(f"run_eval: {len(cases)} cases against model={model}\n")

    substr_hits = 0
    cited_hits = 0
    faith_scores = []

    for c in cases:
        print(f"\n=== {c['q']} ===")
        result = ask(client, model, c["q"])
        print(f"  answer: {result['answer'][:200]}")
        print(f"  citations: {result['citations']}")
        print(f"  retrieved: {result['retrieved_ids']}")

        # Metric 1: must_contain substrings in answer (relevance proxy)
        substr_ok = all(s.lower() in result["answer"].lower() for s in c["must_contain"])
        print(f"  {'✓' if substr_ok else '✗'} must_contain: {c['must_contain']}")
        if substr_ok:
            substr_hits += 1

        # Metric 2: at least one citation was in the retrieved set
        cited_ok = bool(result["citations"]) and all(cite in result["retrieved_ids"] for cite in result["citations"])
        print(f"  {'✓' if cited_ok else '✗'} citations point to retrieved chunks")
        if cited_ok:
            cited_hits += 1

        # Metric 3: faithfulness via LLM-judge
        try:
            verdict = judge_faithfulness(client, model, c["q"], result["answer"], result["retrieved"])
            score = verdict["overall_faithfulness_score"]
            faith_scores.append(score)
            print(f"  faithfulness: {score:.2f}  reasoning: {verdict['reasoning'][:150]}")
        except NotImplementedError as e:
            print(f"  faithfulness: TODO not filled ({e})")

    n = len(cases)
    avg_faith = sum(faith_scores) / max(len(faith_scores), 1) if faith_scores else None
    print(f"\n{'='*70}\nSummary:")
    print(f"  must_contain hits: {substr_hits}/{n} ({100*substr_hits/n:.0f}%)")
    print(f"  citation_valid hits: {cited_hits}/{n} ({100*cited_hits/n:.0f}%)")
    if avg_faith is not None:
        print(f"  avg faithfulness: {avg_faith:.2f}")
    else:
        print(f"  avg faithfulness: (skipped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
