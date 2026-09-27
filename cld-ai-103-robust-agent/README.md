# CLD-AI-103 Lesson 6 — Robust agent with error handling

Third CLD-AI-103 hands-on. Extends L4's 4-tool agent with production-grade defenses: (a) safe_execute wrapper turning exceptions into tool_result blocks, (b) retry with exponential backoff for transient errors, (c) max_iterations + max_tool_calls circuit breakers. Tools deliberately fail transiently under load so you see the retry recover.

## Files

```
cld-ai-103-robust-agent/
  README.md, .env.example, .gitignore, requirements.txt
  data/customers.json
  src/
    verify_env.py
    flaky_tools.py         # COMPLETE: 4 tools with configurable failure injection.
    safe_agent.py          # Exercise 2 skeleton — TODO: safe_execute + retry wrapper + circuit breakers.
    test_robustness.py     # Exercise 3 — 4 stress scenarios (transient failures, permanent failure, budget exhaustion).
```
