# AI-3026 Lesson 6 — Extend an agent with MCP tools

Python starter for the Halcyon Assist spare-parts + repair-cost lookup agent. You publish two tools as a Model Context Protocol (MCP) server using `fastmcp`, then consume them from a Foundry agent via `MCPTool`.

## Scenario

Halcyon's auto-claims adjusters need to attach a preliminary parts + labor estimate to every collision claim before it goes to the shop network. Rather than build the lookup logic *into* one agent (which trapped it there), you host it as a **portable MCP server** — any agent, in any framework, in any process can now consume it. In L6 you host the server locally and point a Foundry agent at it; in production the same server would be a shared platform primitive.

## Files

```
ai3026-mcp-tools/
  README.md
  .env.example
  .gitignore
  requirements.txt          # Reference — all installed in the lab container.
  src/
    verify_env.py           # Smoke test — one AIProjectClient round-trip.
    mcp_server/
      halcyon_parts_server.py   # fastmcp server exposing lookup_part + estimate_repair_cost.
    mcp_client/
      halcyon_repair_agent.py   # Foundry agent w/ MCPTool pointing at the local server.
  data/
    parts.json              # 20 Halcyon-relevant auto/property spare-parts records.
```

## How to run

1. `az login --use-device-code`
2. Copy `.env.example` → `.env`.
3. `python src/verify_env.py`
4. **Terminal 1**: start the MCP server — `python src/mcp_server/halcyon_parts_server.py` (listens on `http://127.0.0.1:8123/mcp` by default).
5. **Terminal 2**: run the Foundry agent client — `python src/mcp_client/halcyon_repair_agent.py`.

## Authentication

Client → Foundry uses `DefaultAzureCredential`. The MCP server → agent link is unauthenticated on localhost (production would front it with mTLS or an API gateway).

## Notes

- **Env-var naming deviates from SkillMeUp canonical.** `FOUNDRY_PROJECT_ENDPOINT` + `FOUNDRY_MODEL` per MS Learn's `mslearn-ai-agents` convention. Deliberate — matches the exam-prep material.
- **Model pin:** `gpt-5` version `2025-08-07`.
- **`requirements.txt` reference-only.** `mcp` + `fastmcp` were added to the `python-ai` container specifically for this lesson (2026-08-23 Dockerfile bump).
- The MCP server has **no auth** on localhost — do NOT expose it to a public network without a reverse proxy.
