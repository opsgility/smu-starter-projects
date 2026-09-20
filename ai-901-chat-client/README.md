# ai-901-chat-client — lightweight Foundry chat client

Starter for AI-901 Obj 2 Part II (Foundry SDK — Building a Chat Client). Plain single-turn chat scaffold. The exercise has you:

1. Add a system prompt.
2. Add a conversation history buffer (multi-turn).
3. Switch to streaming responses.
4. Keep `DefaultAzureCredential` keyless auth.

## What's here
- `src/chat.py` — minimal REPL that sends each user message as a fresh (single-turn) call and prints the model reply. No system prompt, no history, no streaming yet — those are the exercise.

## Env vars
Copy `.env.example` → `.env` and fill in `FOUNDRY_PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME`.

## Run
```
python src/chat.py
```
Type messages at the prompt, `Ctrl+C` to exit.
