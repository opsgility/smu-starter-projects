"""Orion daily-digest workload — apply every optimization.

Baseline: 100 tickets/day, Sonnet, no cache, no batch, no routing.
Goal: cut cost 80%+ while keeping accuracy > 90%.
"""

import time, random
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

# Padded to ~6000 tokens. Haiku 4.5's prompt-cache minimum is 4096 tokens
# (Sonnet is 1024). Smaller cached prefixes silently return 0/0 for
# cache_creation/read on Haiku. Live-lab measurements confirmed a ~2800-token
# prefix still returned 0/0; * 160 lands safely above the 4096 floor.
SYSTEM_PROMPT = ("You are the Orion ticket triager. Classify each ticket as "
                 "bug/billing/feature/howto. Then rate urgency 1-5. "
                 "Reply as: LABEL,URGENCY. Nothing else. ") * 160

TICKETS = ["Login broken", "Export CSV please", "Refund my Aug charge",
           "Feature: dark mode", "API 500 error", "Password reset", "Slow load",
           "Trial ended", "Missing data", "SSO broken"] * 2  # 20 tickets by default; scale up in the exercise


def call_haiku_cached(ticket):
    return client.messages.create(
        model="claude-haiku-4-5", max_tokens=20,
        system=[{"type": "text", "text": SYSTEM_PROMPT,
                 "cache_control": {"type": "ephemeral", "ttl": "5m"}}],
        messages=[{"role": "user", "content": ticket}])


def with_retry(fn, ticket, max_attempts=4):
    for attempt in range(max_attempts):
        try:
            return fn(ticket)
        except anthropic.RateLimitError:
            time.sleep(min(30, 2 ** attempt + random.random()))
    return None


def main():
    t0 = time.perf_counter()
    total_in = total_out = cache_read = cache_write = 0
    results = []
    for tkt in TICKETS:
        r = with_retry(call_haiku_cached, tkt)
        if r is None:
            results.append((tkt, "SHED"))
            continue
        text = next((b.text for b in r.content if b.type == "text"), "").strip()
        results.append((tkt, text))
        total_in += r.usage.input_tokens
        total_out += r.usage.output_tokens
        cache_read += getattr(r.usage, "cache_read_input_tokens", 0)
        cache_write += getattr(r.usage, "cache_creation_input_tokens", 0)

    elapsed = time.perf_counter() - t0
    cost = (total_in * 0.80 + cache_write * 1.00 + cache_read * 0.08 + total_out * 4.00) / 1e6
    ok = sum(1 for _, r in results if r != "SHED" and "," in r)
    print(f"\n=== {len(TICKETS)} tickets ===")
    print(f"time:        {elapsed:.1f}s")
    print(f"tokens:      in={total_in} out={total_out} cache_read={cache_read} cache_write={cache_write}")
    print(f"cost:        ${cost:.4f}")
    print(f"successful:  {ok}/{len(TICKETS)}")
    print(f"\n(Compare vs Sonnet no-cache: ~$1.50 for the same 100 tickets.)")


if __name__ == "__main__":
    main()
