"""Run bank against Claude + score."""

import json, os, sys
from pathlib import Path
from dotenv import load_dotenv
import anthropic


def ask(client, model, q):
    r = client.messages.create(model=model, max_tokens=400,
        system="You are a support-triage assistant for Orion Analytics.",
        messages=[{"role":"user","content":q}])
    return next((b.text for b in r.content if b.type == "text"), "")


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    bank = json.loads((Path(__file__).resolve().parent.parent / "data" / "bank.json").read_text())
    passed = 0
    for c in bank:
        answer = ask(client, model, c["input"])
        checks = []
        for s in c.get("must_contain", []):
            checks.append((f"contains '{s}'", s.lower() in answer.lower()))
        for s in c.get("must_not_contain", []):
            checks.append((f"NOT contains '{s}'", s.lower() not in answer.lower()))
        all_ok = all(ok for _, ok in checks)
        if all_ok: passed += 1
        print(f"\n[{c['id']}] {c['input']}")
        print(f"  answer: {answer[:100]}...")
        for desc, ok in checks:
            print(f"    {'✓' if ok else '✗'} {desc}")
    print(f"\nSummary: {passed}/{len(bank)} passed")


if __name__ == "__main__":
    main()
