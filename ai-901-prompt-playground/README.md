# AI-901 Lesson 4 — Prompt Playground Starter

Scaffold for Lesson 4. You'll craft prompts in the Foundry Playground and then run the same prompts programmatically via the Inference SDK.

## Files

- `prompts/system_assistant.md` — starter system prompt (TODO markers for you to edit)
- `prompts/user_queries.md` — a small set of user queries to run against each prompt
- `eval.py` — harness that runs each prompt + query combo against a deployed model

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
python eval.py
```
