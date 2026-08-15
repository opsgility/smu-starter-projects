# ai-901-agent-client — Foundry single-agent scaffold

Starter for AI-901 Obj 2 Part III (Single-Agent Solutions in Foundry). Builds a single Foundry agent with the Microsoft Agent Framework (`agent-framework` + `FoundryChatClient`) and gives you a stubbed function tool. The exercise has you:

1. Verify the scaffold with `--create`.
2. Extend the placeholder `get_store_hours(store_id)` function tool.
3. Implement `chat_once` — call `await agent.run(message)` and print the reply.
4. Inspect `result.messages` to see the tool-call lifecycle.

## What's here
- `src/agent.py` — `build_agent()` constructs an ephemeral `Agent` backed by `FoundryChatClient` with the placeholder `get_store_hours` tool. `chat_once()` is the stub the exercise has you implement.

Agents in Agent Framework are in-process and ephemeral — there is no persistent `AGENT_ID` you need to capture. If you want a service-managed Foundry agent, use `FoundryAgent` instead (see MS Learn: [Foundry Agents](https://learn.microsoft.com/agent-framework/support/upgrade/python-2026-significant-changes)).

## Env vars
Copy `.env.example` → `.env` and set your Foundry project endpoint and deployed model name (`FOUNDRY_MODEL`).

## Run
```
python src/agent.py --create
python src/agent.py --chat "What are the store hours for store 42?"
```
(The `--chat` branch is the part you implement.)

## References
- [Agent Framework — Your first agent](https://learn.microsoft.com/agent-framework/get-started/your-first-agent)
- [Function calling with Agent Framework](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/function-calling)
