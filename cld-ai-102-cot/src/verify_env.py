"""Smoke test — same shape as L2 and L4.

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
        print("verify_env: FAIL — ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        return 1

    client = anthropic.Anthropic()
    t0 = time.perf_counter()
    try:
        resp = client.messages.create(
            model=model, max_tokens=12,
            messages=[{"role": "user", "content": "Say the word ready and nothing else."}],
        )
    except anthropic.APIError as e:
        print(f"verify_env: FAIL — {e}", file=sys.stderr)
        return 1

    latency_ms = int((time.perf_counter() - t0) * 1000)
    text = next((b.text for b in resp.content if b.type == "text"), "").strip()
    print(f"verify_env: OK — {model} responded in {latency_ms} ms")
    print(f"  response: {text!r}")
    print(f"  usage:    input={resp.usage.input_tokens} output={resp.usage.output_tokens}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
