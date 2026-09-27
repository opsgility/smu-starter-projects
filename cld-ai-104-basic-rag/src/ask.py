"""Exercise 3 — run 8 questions through the RAG pipeline + assert expected chunks were retrieved."""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rag import rag_answer


QUESTIONS = [
    {"q": "What's the SLA for a Sev-1 outage?", "expected_ids": ["sla-1"]},
    {"q": "How long can we refund after 30 days?", "expected_ids": ["refund-1"]},
    {"q": "What rate limit does /v2/analytics have?", "expected_ids": ["api-1"]},
    {"q": "How do I get the SOC 2 report?", "expected_ids": ["compliance-2"]},
    {"q": "Can a support engineer apply a $150 credit without approval?", "expected_ids": ["refund-2"]},
    {"q": "What's Orion's EU data residency requirement?", "expected_ids": ["compliance-1"]},
    {"q": "How do I get an auth token?", "expected_ids": ["api-3"]},
    {"q": "What's the default customer data retention?", "expected_ids": ["compliance-3"]},
]


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    print(f"ask: {len(QUESTIONS)} questions against model={model}\n")

    retrieved_hits = 0
    cited_hits = 0
    for q in QUESTIONS:
        print(f"\n=== {q['q']} ===")
        try:
            r = rag_answer(client, model, q["q"], k=5)
        except NotImplementedError as e:
            print(f"  TODO not filled: {e}"); continue

        print(f"  answer: {r['answer'][:200]}...")
        print(f"  citations: {r['citations']}")
        print(f"  retrieved_ids: {r['retrieved_ids']}")

        # Check 1: expected id was in the retrieved top-k
        retrieved_ok = all(eid in r["retrieved_ids"] for eid in q["expected_ids"])
        # Check 2: expected id appears in Claude's citations
        cited_ok = all(eid in r["citations"] for eid in q["expected_ids"])
        print(f"  {'✓' if retrieved_ok else '✗'} retrieved expected: {q['expected_ids']}")
        print(f"  {'✓' if cited_ok else '✗'} cited expected: {q['expected_ids']}")
        if retrieved_ok: retrieved_hits += 1
        if cited_ok: cited_hits += 1

    n = len(QUESTIONS)
    print(f"\nSummary:  retrieved {retrieved_hits}/{n} ({100*retrieved_hits/n:.0f}%)  "
          f"cited {cited_hits}/{n} ({100*cited_hits/n:.0f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
