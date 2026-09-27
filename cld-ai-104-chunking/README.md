# CLD-AI-104 Lesson 6 — Chunking strategy experiment

Third CLD-AI-104 hands-on. Take one long Orion runbook doc, chunk it three ways (fixed-size 200, 500, 1000; recursive 500 with overlap; single-doc-no-split), embed each variant, run 6 test queries against each index, report retrieval precision + recall per strategy.

## Files
```
cld-ai-104-chunking/
  README.md, .env.example, .gitignore, requirements.txt
  data/runbook.md            # 1 long doc (~3000 chars, multiple sections)
  data/queries.json          # 6 queries with expected-content markers
  src/
    verify_env.py
    chunkers.py              # COMPLETE: fixed_size + recursive_split.
    experiment.py            # Exercise 2 — TODO: run 5 chunking configs, score each.
```
