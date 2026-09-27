"""Batch extraction with concurrency + retry."""

import json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import anthropic


SCHEMA = {"name":"submit",
  "input_schema":{"type":"object",
    "properties":{"category":{"type":"string","enum":["Billing","Technical","Feature Request","Other"]},
                  "urgency":{"type":"string","enum":["low","normal","urgent"]}},
    "required":["category","urgency"], "additionalProperties":False}}


TICKETS = [
    "Dashboard down 40min", "Charged twice Sept renewal", "Row-level perms please",
    "429 errors on /v2/analytics blocking", "SSO for our security review",
    "Just saying thanks!", "How do I add users?", "Suspended account refund",
    "Timezone bug in scheduler", "SOC 2 report request",
]


def extract_with_retry(client, model, text: str, max_attempts: int = 4) -> dict:
    """TODO: retry on transient exceptions with exponential backoff.
    HINT:
      for attempt in range(1, max_attempts+1):
          try:
              resp = client.messages.create(model=model, max_tokens=300,
                  tools=[SCHEMA], tool_choice={"type":"tool","name":"submit"},
                  messages=[{"role":"user","content": f"Classify: {text}"}])
              return dict(next(b.input for b in resp.content if b.type == "tool_use"))
          except anthropic.RateLimitError:
              if attempt == max_attempts: raise
              time.sleep(2**(attempt-1))
    """
    raise NotImplementedError("TODO")


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    t0 = time.perf_counter()
    try:
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda t: extract_with_retry(client, model, t), TICKETS))
    except NotImplementedError as e:
        print(f"TODO: {e}"); return 1
    elapsed = time.perf_counter() - t0

    for t, r in zip(TICKETS, results):
        print(f"  {t[:40]:<42} → {r}")
    print(f"\nProcessed {len(TICKETS)} tickets in {elapsed:.1f}s ({len(TICKETS)/elapsed:.1f} tickets/sec)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
