"""Extraction pipeline + per-field eval."""

import json, os, sys
from pathlib import Path
from dotenv import load_dotenv
import anthropic


SCHEMA = {"name":"submit",
  "input_schema":{"type":"object",
    "properties":{"category":{"type":"string","enum":["Billing","Technical","Feature Request","Other"]},
                  "urgency":{"type":"string","enum":["low","normal","urgent"]}},
    "required":["category","urgency"], "additionalProperties":False}}


def extract(client, model, text):
    resp = client.messages.create(model=model, max_tokens=200,
        tools=[SCHEMA], tool_choice={"type":"tool","name":"submit"},
        messages=[{"role":"user","content": f"Classify: {text}"}])
    return dict(next(b.input for b in resp.content if b.type == "tool_use"))


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    cases = json.loads((Path(__file__).resolve().parent.parent / "data" / "gold.json").read_text())
    field_hits = {"category": 0, "urgency": 0}
    exact = 0

    for c in cases:
        pred = extract(client, model, c["input"])
        gold = c["gold"]
        for f in field_hits:
            if pred.get(f) == gold.get(f):
                field_hits[f] += 1
        if pred == gold:
            exact += 1
        print(f"  {c['input'][:40]:<42} pred={pred}  gold={gold}  {'✓' if pred == gold else '✗'}")

    n = len(cases)
    print(f"\n=== SCORECARD ===")
    for f, h in field_hits.items():
        print(f"  per-field precision on {f}: {h}/{n} ({100*h/n:.0f}%)")
    print(f"  exact-record match: {exact}/{n} ({100*exact/n:.0f}%)")


if __name__ == "__main__":
    main()
