# ai-901-prompt-playground — iterate on prompts + tiny eval harness

Starter for AI-901 Obj 2 Part I (Prompt Engineering & Portal Chat). Three sample system prompts, a runner that feeds a user message, and a 3-case eval harness.

## What's here
- `prompts/helpful-assistant.txt` — generic helpful assistant.
- `prompts/strict-classifier.txt` — one-label classifier, refuses to explain.
- `prompts/json-responder.txt` — must respond only with well-formed JSON.
- `src/run_prompt.py` — takes `--prompt <file>` and `--message <text>`, prints the model response.
- `src/eval.py` — runs 3 built-in test cases against each prompt file and reports pass/fail.

## Env vars
Copy `.env.example` → `.env`. Needs `FOUNDRY_PROJECT_ENDPOINT` + `MODEL_DEPLOYMENT_NAME`.

## Run
```
python src/run_prompt.py --prompt prompts/helpful-assistant.txt --message "What's the capital of France?"
python src/eval.py
```
