# CLD-AI-103 Lesson 8 — Structured JSON extraction pipeline

Fourth CLD-AI-103 hands-on. Build an extraction pipeline that consumes 15 Orion tickets, produces schema-valid warehouse-ready records via the tool_use pattern, and demonstrates the failure mode when the schema is loosened.

## Files

```
cld-ai-103-json-extract/
  README.md, .env.example, .gitignore, requirements.txt
  data/tickets.json
  src/
    verify_env.py
    schemas.py            # COMPLETE: STRICT_SCHEMA + LOOSE_SCHEMA (for ablation).
    extract.py            # Exercise 2 skeleton — TODO: implement tool_use extraction.
    validate.py           # Exercise 3 script — validates every record + reports failure rate.
```
