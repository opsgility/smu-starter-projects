"""AFTER: Haiku + cached system prompt."""

import time
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

# Padded to ~4800 tokens. Haiku 4.5's prompt-cache minimum is 4096 tokens —
# a smaller cached prefix silently returns 0/0 for cache_creation/read.
SYSTEM = """You are the Orion support triager. """ * 800

TICKETS = [
    "Login broken",
    "How to export CSV",
    "Refund please",
    "Feature: dark mode",
    "500 error on API",
] * 5

t0 = time.perf_counter()
total_in = total_out = cache_read = cache_write = 0
for t in TICKETS:
    r = client.messages.create(
        model="claude-haiku-4-5", max_tokens=50,
        system=[{"type": "text", "text": SYSTEM,
                 "cache_control": {"type": "ephemeral", "ttl": "5m"}}],
        messages=[{"role": "user", "content": f"Classify: {t}. One word."}])
    total_in += r.usage.input_tokens
    total_out += r.usage.output_tokens
    cache_read += getattr(r.usage, "cache_read_input_tokens", 0)
    cache_write += getattr(r.usage, "cache_creation_input_tokens", 0)

elapsed = time.perf_counter() - t0
# Haiku pricing: $0.80/M in, $4/M out, cache read 0.1x
cost = (total_in * 0.80 + cache_write * 1.00 + cache_read * 0.08 + total_out * 4.00) / 1e6
print(f"AFTER:  {elapsed:.1f}s, {total_in} in / {total_out} out, "
      f"cache={cache_read} read / {cache_write} write, ${cost:.4f}")
