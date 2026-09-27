"""BEFORE: expensive path — Sonnet on every call, no cache."""

import time
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

SYSTEM = """You are the Orion support triager. """ * 200  # ~1200 tokens padding

TICKETS = [
    "Login broken",
    "How to export CSV",
    "Refund please",
    "Feature: dark mode",
    "500 error on API",
] * 5  # 25 total

t0 = time.perf_counter()
total_in = total_out = 0
for t in TICKETS:
    r = client.messages.create(
        model="claude-sonnet-5", max_tokens=50,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Classify: {t}. One word."}])
    total_in += r.usage.input_tokens
    total_out += r.usage.output_tokens

elapsed = time.perf_counter() - t0
cost = total_in * 3/1e6 + total_out * 15/1e6
print(f"BEFORE: {elapsed:.1f}s, {total_in} in / {total_out} out, ${cost:.4f}")
