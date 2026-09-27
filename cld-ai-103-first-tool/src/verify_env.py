"""Smoke test."""
import os, sys, time
from dotenv import load_dotenv
import anthropic

def main() -> int:
    load_dotenv()
    if not os.environ.get("ANTHROPIC_API_KEY", "").strip() or os.environ.get("ANTHROPIC_API_KEY", "").startswith("<"):
        print("verify_env: FAIL — key not set", file=sys.stderr); return 1
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    c = anthropic.Anthropic()
    t0 = time.perf_counter()
    r = c.messages.create(model=model, max_tokens=12, messages=[{"role":"user","content":"Say ready."}])
    text = next((b.text for b in r.content if b.type == "text"), "")
    print(f"verify_env: OK — {model} responded in {int((time.perf_counter()-t0)*1000)} ms  usage=in{r.usage.input_tokens}/out{r.usage.output_tokens}")
    print(f"  response: {text.strip()!r}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
