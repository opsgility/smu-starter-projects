# ai-901-agent-client — Foundry single-agent scaffold

Starter for AI-901 Obj 2 Part III (Single-Agent Solutions in Foundry). Creates a single Foundry agent via the SDK and gives you a stubbed function tool. The exercise has you:

1. Create the agent in the Foundry portal first, then reference it by `AGENT_ID`.
2. Add a real function tool (e.g., `get_store_hours(store_id)`).
3. Send a message on a thread and poll the run until complete.
4. Inspect tool calls vs. assistant messages.

## What's here
- `src/agent.py` — `create_agent()` builds an agent with a simple instruction and the placeholder `get_store_hours` tool. `chat_once()` is a stub that the exercise has you implement (create thread → post message → create run → poll → read).

## Env vars
Copy `.env.example` → `.env`. You will set `AGENT_ID` after creating the agent in the portal (exercise step 2).

## Run
```
python src/agent.py --create
python src/agent.py --chat "What are the store hours for store 42?"
```
(The `--chat` branch is the part you implement.)
