# CLD-AI-103 Lesson 2 — Your first Claude tool-calling agent

Starter for the first hands-on lab in **Building Claude Agents**. You implement a working tool-calling agent against Orion Analytics' fake customer database, verify Claude reasons about the tool, calls it, reads the result, and produces a correct final answer.

## Scenario

Orion's team lead needs an agent that decides whether to refund a customer based on their actual account status — not just the ticket text. You'll wire up one tool (`get_customer_status`), the agent loop, and prove it works on a suspended-account refund request where the correct answer requires the tool result.

## Files

```
cld-ai-103-first-tool/
  README.md
  .env.example
  .gitignore
  requirements.txt
  data/customers.json       # 4 fake customers: mixed tiers + statuses
  src/
    verify_env.py           # Smoke test.
    tools.py                # COMPLETE: get_customer_status function + tool schema.
    agent.py                # Exercise 2 skeleton — TODO: build the agent loop.
    test_agent.py           # Exercise 3 script — 4 test cases exercising different behaviors.
```

## How to run

Same PythonAI + Claude proxy shape as CLD-AI-102 labs. `python src/verify_env.py`, then Exercises 1-3.

## What you'll practice

- Wiring a Python function to a Claude tool schema.
- Implementing the tool_use → tool_result loop.
- Using `stop_reason` for the exit condition.
- Reading a tool_use block's `input` and dispatching to the right function.
- Debugging a bug where the loop never exits or fires the wrong tool.
