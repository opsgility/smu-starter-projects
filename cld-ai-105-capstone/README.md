# CLD-AI-105 L10 — Capstone: Orion multi-server MCP agent

Wire everything: 2 in-process MCP servers (orion + runbook), approval gate, tool aggregation, and Claude driving the agent loop. Answer a support-triage question that requires calls to BOTH servers.

## Files
- `orion_server.py` — customer + ticket tools.
- `runbook_server.py` — resource-shape SLA docs.
- `capstone_agent.py` — Claude + multi-server + approval, all together. TODO wires the loop.
