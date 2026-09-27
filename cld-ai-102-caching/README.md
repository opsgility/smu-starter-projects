# CLD-AI-102 Lesson 8 — Measure prompt cache cost + throughput

Starter for the fourth hands-on lab in **Prompt Engineering with Claude**. You take L4's few-shot classifier, add `cache_control` markers on the stable content (system + examples), fire 20 tickets in a tight burst, and read `cache_read_input_tokens` / `cache_creation_input_tokens` from the response to confirm you got the ~90% savings L7 predicted. Ex 3 breaks the cache with a per-call timestamp above the marker so you see the failure mode with your own eyes.

## Scenario

Same Orion Analytics setup. Your L4 classifier is at 95% accuracy but the Claude bill just crossed $900/month on this workload alone. Team lead asked you to test the prompt caching described in L7 and report back the actual cost delta on 20 sequential tickets.

## Files

```
cld-ai-102-caching/
  README.md                       # this file
  .env.example                    # ANTHROPIC_API_KEY (injected) + ANTHROPIC_MODEL
  .gitignore                      # .env, __pycache__
  requirements.txt                # Manifest — anthropic + python-dotenv preinstalled.
  data/tickets.json               # Same 20 tickets from L4 (10 typical + 10 edge).
  src/
    verify_env.py                 # Smoke test.
    classify_uncached.py          # L4's few-shot baseline (COMPLETE, do not edit).
    classify_cached.py            # Exercise 2 skeleton — TODO: add cache_control markers.
    classify_cached_broken.py     # Exercise 3 skeleton — TODO: break cache with a timestamp.
    measure_caching.py            # Exercise 4 runner — fires 20 tickets x 3 versions, reports cache metrics + $.
```

## How to run

Standard L2 shape: `python src/verify_env.py`, then work Exercises 1-4.

## What you'll practice

- Adding `cache_control: {"type": "ephemeral"}` markers on the system prompt + few-shot examples block.
- Reading `response.usage.cache_read_input_tokens` and `.cache_creation_input_tokens` to confirm cache hits.
- Diagnosing cache misses (the "timestamp above the marker" anti-pattern).
- Converting cache-metric numbers into monthly-cost estimates for 200,000-ticket workloads.

## Notes

- All model IDs from `ANTHROPIC_MODEL` env — never hardcoded.
- 5-minute TTL applies. If you re-run measure_caching.py more than 5 minutes apart, the cache re-warms from cold on the second run.
- Rate limits: firing 60 calls (20 × 3) in a burst is well within Claude's per-account limits.
