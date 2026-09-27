"""Stream vs block latency comparison."""

import time
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

PROMPT = "Explain how a load balancer works in about 300 words for an Orion Analytics ops engineer."


def blocking():
    t0 = time.perf_counter()
    r = client.messages.create(model="claude-sonnet-5", max_tokens=800,
        messages=[{"role":"user","content":PROMPT}])
    text = next((b.text for b in r.content if b.type == "text"), "")
    total = time.perf_counter() - t0
    print(f"\n[BLOCKING] first token at: {total:.2f}s (no earlier signal)")
    print(f"[BLOCKING] total chars: {len(text)}")


def streaming():
    t0 = time.perf_counter()
    first_token_time = None
    total_chars = 0
    with client.messages.stream(model="claude-sonnet-5", max_tokens=800,
        messages=[{"role":"user","content":PROMPT}]) as stream:
        for chunk in stream.text_stream:
            if first_token_time is None:
                first_token_time = time.perf_counter() - t0
            total_chars += len(chunk)
    total = time.perf_counter() - t0
    print(f"\n[STREAM]   first token at: {first_token_time:.2f}s")
    print(f"[STREAM]   total done at:   {total:.2f}s")
    print(f"[STREAM]   total chars: {total_chars}")


if __name__ == "__main__":
    blocking()
    streaming()
