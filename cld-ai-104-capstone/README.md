# CLD-AI-104 Lesson 10 — RAG capstone

Capstone for CLD-AI-104. Full production RAG pipeline over Orion's knowledge base:
- Recursive chunker (L5-L6)
- Hybrid retriever with RRF (L7-L8)
- Cited Claude answers (L1-L2)
- Faithfulness + relevance evaluation via LLM-judge (L9)

## Files
```
cld-ai-104-capstone/
  README.md, .env.example, .gitignore, requirements.txt
  data/corpus.md               # ~4000 chars of Orion docs
  data/eval_cases.json         # 10 Q+expected_answer_substring test cases
  src/
    verify_env.py
    pipeline.py                # COMPLETE: chunker + retriever + Claude generation
    faithfulness_judge.py      # Exercise 2 — TODO: LLM-judge for faithfulness
    run_eval.py                # Exercise 3 — full 4-dimension eval scorecard
```
