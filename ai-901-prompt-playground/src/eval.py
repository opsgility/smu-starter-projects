"""Tiny eval harness — 3 test cases per prompt."""
from __future__ import annotations

import json
from pathlib import Path

from run_prompt import run

HERE = Path(__file__).parent.parent

CASES = {
    "prompts/helpful-assistant.txt": [
        ("What's the capital of France?", lambda r: "paris" in r.lower()),
        ("2 + 2 = ?", lambda r: "4" in r),
        ("Who wrote Pride and Prejudice?", lambda r: "austen" in r.lower()),
    ],
    "prompts/strict-classifier.txt": [
        ("I love this product!", lambda r: r.strip().upper() == "POSITIVE"),
        ("This is the worst thing ever.", lambda r: r.strip().upper() == "NEGATIVE"),
        ("It's fine, I guess.", lambda r: r.strip().upper() in {"NEUTRAL", "NEGATIVE", "POSITIVE"}),
    ],
    "prompts/json-responder.txt": [
        ("What is the capital of Japan?", lambda r: _is_json(r)),
        ("Is the sky blue?", lambda r: _is_json(r)),
        ("Name a planet.", lambda r: _is_json(r)),
    ],
}


def _is_json(text: str) -> bool:
    try:
        obj = json.loads(text.strip())
        return "answer" in obj and "confidence" in obj
    except Exception:
        return False


def main() -> None:
    total = passed = 0
    for prompt_rel, cases in CASES.items():
        print(f"\n=== {prompt_rel}")
        for message, check in cases:
            total += 1
            try:
                out = run(str(HERE / prompt_rel), message, temperature=0.0)
                ok = bool(check(out))
            except Exception as exc:  # noqa: BLE001
                ok = False
                out = f"ERROR: {exc}"
            passed += int(ok)
            flag = "PASS" if ok else "FAIL"
            print(f"  [{flag}] {message!r:<40} → {out[:60]!r}")
    print(f"\n{passed}/{total} passed")


if __name__ == "__main__":
    main()
