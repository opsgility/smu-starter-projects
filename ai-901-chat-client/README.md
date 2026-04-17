# AI-901 Lesson 5 — Chat Client Starter (Foundry SDK)

Scaffold for Lesson 5. You'll build a lightweight chat client that calls a Foundry-deployed chat model through the Foundry SDK.

## Files

- `chat.py` — one-shot chat (single user message → single response)
- `conversation.py` — multi-turn chat that keeps history

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
python chat.py "Hello"
python conversation.py
```
