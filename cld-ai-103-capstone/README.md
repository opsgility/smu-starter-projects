# CLD-AI-103 Lesson 10 — Full customer-support agent capstone

Capstone for **Building Claude Agents**. Combines every technique from L1-L9:

- **L1-L4:** tool_use loop + 4-tool orchestration (get_customer_status, search_recent_tickets, apply_refund, escalate_to_human)
- **L6:** safe_execute + retry + circuit breakers
- **L8:** structured JSON action record via tool_use schema
- **L9:** eval harness with 15 scenarios + deterministic rules + LLM-as-judge

## Files

```
cld-ai-103-capstone/
  README.md, .env.example, .gitignore, requirements.txt
  data/
    customers.json
    tickets.json
    eval_cases.json          # 15 test cases: happy-path + edge + adversarial
  src/
    verify_env.py
    tools.py                 # COMPLETE: 4 tools with safe execution.
    action_schema.py         # COMPLETE: JSON schema for final action record.
    production_agent.py      # Exercise 2 — TODO: wire everything together.
    eval_harness.py          # Exercise 3 — TODO: implement scoring + LLM-judge.
    run_full_eval.py         # Exercise 4 — end-to-end harness run.
```
