# AI-103 Lesson 8 — Agent Service Basics Starter

Scaffold for the Azure AI Agent Service: build a "Northwind concierge" agent with three
function tools (`get_weather`, `calculate`, `lookup_inventory`), threaded conversations,
and auto function-call execution.

## Files

- `app/agent.py` — agent + thread + run management
- `app/functions.py` — Python implementations exposed as tools
- `test_client.py` — sends a multi-turn conversation through the agent

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
python test_client.py
```
