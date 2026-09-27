# CLD-AI-103 Lesson 4 — Multi-step tool orchestration agent

Second CLD-AI-103 hands-on. Extends L2's single-tool agent to FOUR tools (get_customer_status, search_recent_tickets, apply_refund, escalate_to_human). Watch Claude chain 2-4 tool calls per scenario, parallelize independent lookups, and produce a final action recommendation.

## Files

```
cld-ai-103-multi-tool/
  README.md, .env.example, .gitignore, requirements.txt
  data/customers.json, data/tickets.json
  src/
    verify_env.py
    tools.py                 # COMPLETE: 4 tools + implementations.
    agent_sequential.py      # Exercise 2 skeleton — TODO: extend loop from L2 shape.
    agent_parallel.py        # Exercise 3 skeleton — TODO: parallelize with ThreadPoolExecutor.
    measure_orchestration.py # Exercise 4 — runs 5 scenarios, reports iteration count + latency.
```

## What you'll practice

- 4-tool orchestration with Claude deciding the sequence.
- ThreadPoolExecutor parallelization for independent lookups.
- Reading iteration counts + tool_use patterns from real traces.
- Debugging when Claude picks the wrong tool sequence (usually a tool description problem).
