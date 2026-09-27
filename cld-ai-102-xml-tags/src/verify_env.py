"""Smoke test — confirms the lab environment is wired up correctly.

Reads ANTHROPIC_API_KEY and ANTHROPIC_MODEL from the environment (or .env),
issues a single 12-token round-trip to Claude, and exits 0 on success.

Run: `python src/verify_env.py`
"""

import os
import sys
import time

from dotenv import load_dotenv
import anthropic


def main() -> int:
    load_dotenv()

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    if not api_key or api_key.startswith("<"):
        print(
            "verify_env: FAIL — ANTHROPIC_API_KEY is not set (or still the placeholder value).",
            file=sys.stderr,
        )
        print(
            "In the SkillMeUp lab environment the proxy should inject the key automatically. "
            "If you're running locally, copy .env.example to .env and paste a key from "
            "https://platform.claude.com/settings/keys.",
            file=sys.stderr,
        )
        return 1

    client = anthropic.Anthropic()
    t0 = time.perf_counter()
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=12,
            messages=[{"role": "user", "content": "Say the word ready and nothing else."}],
        )
    except anthropic.APIError as e:
        print(f"verify_env: FAIL — Anthropic API error: {e}", file=sys.stderr)
        return 1

    latency_ms = int((time.perf_counter() - t0) * 1000)
    # resp.content is a list of typed blocks. Adaptive-thinking models
    # (Opus 5.5, sometimes Fable 5.1) may emit a `ThinkingBlock` FIRST,
    # so filter for the text block explicitly instead of assuming [0] is
    # the text — otherwise a swap to those models will crash with
    # `AttributeError: 'ThinkingBlock' object has no attribute 'text'`.
    text = next((b.text for b in resp.content if b.type == "text"), "").strip()
    tokens_in = resp.usage.input_tokens
    tokens_out = resp.usage.output_tokens

    print(f"verify_env: OK — {model} responded in {latency_ms} ms")
    print(f"  response: {text!r}")
    print(f"  usage:    input={tokens_in} tokens, output={tokens_out} tokens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
