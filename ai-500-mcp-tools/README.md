# AI-500 L7 — Build MCP tool servers for market data and compliance checks

Python starter for the Ridgevault Financial market-data + compliance MCP tools lab. You build a `fastmcp` server exposing two tools (`get_market_snapshot`, `check_position_limit`), host it as an HTTP-triggered Azure Function, and wire the deployed endpoint into two Foundry agents (`investment_researcher`, `compliance_officer`) via `HostedMcpTool`.

## Scenario

Ridgevault Financial is a wealth-management firm whose advisor stack runs five agents: portfolio analyst, compliance officer, risk assessor, client relations, and investment researcher. Two of those agents ask the same two questions dozens of times per session — "what is the market snapshot for these tickers?" and "is this proposed position size inside our per-issuer / per-sector limits?". Instead of duplicating the code inside each agent, Ridgevault ships them as ONE MCP server that any agent (in any framework, on any process) can discover and call. In this lab you build the server, host it as an Azure Function so the whole platform can reach it, and attach the deployed endpoint to two agents at once.

## Files

```
ai-500-mcp-tools/
  README.md
  .env.example              # Populated at lab start from the ARM template outputs.
  .gitignore
  requirements.txt          # Reference only — every package is preinstalled in the python-ai container.
  host.json                 # Azure Functions v2 Python worker config.
  function_app.py           # Function App HTTP entry — wraps the fastmcp server for hosting.
  src/
    verify_env.py           # Smoke test — one AIProjectClient round-trip.
    mcp_server/
      ridgevault_tools.py   # fastmcp server with get_market_snapshot + check_position_limit.
      function_wrapper.py   # Reusable ASGI/Starlette adapter used by function_app.py.
    agents/
      investment_researcher.py   # Foundry agent — reads market snapshots and drafts research.
      compliance_officer.py      # Foundry agent — checks position limits before trade suggestions.
  data/
    market-snapshot-sample.json  # 12 ticker snapshots the local tool serves.
    position-limits.json         # Per-issuer + per-sector limits the compliance tool enforces.
```

## How to run

1. `az login --use-device-code` (sign in at `https://microsoft.com/devicelogin`).
2. Copy `.env.example` to `.env` — the values are already set from the ARM template outputs at lab start.
3. `python src/verify_env.py` — confirms `.env` + auth + Foundry endpoint round-trip.
4. **Exercise 2**: run the MCP server locally — `python src/mcp_server/ridgevault_tools.py` (binds `http://127.0.0.1:8123/mcp`).
5. **Exercise 3**: in another terminal, inspect the server — `npx @modelcontextprotocol/inspector http://127.0.0.1:8123/mcp`.
6. **Exercise 4**: deploy to the pre-provisioned Function App — `func azure functionapp publish $FUNCTION_APP_NAME`.
7. **Exercise 5**: run the wired agents — `python src/agents/investment_researcher.py` and `python src/agents/compliance_officer.py` (both point at `$FUNCTION_APP_URL/api/mcp` via `HostedMcpTool`).
8. **Exercise 6**: send the end-to-end portfolio question that triggers both tools.

## Authentication

Client → Foundry authenticates keyless via `DefaultAzureCredential()` (the lab credential is `azureaiuser (Foundry User)` and holds Foundry User + Cognitive Services OpenAI User at subscription scope). The agent → hosted MCP link is HTTPS via the Function App's default `AuthLevel.ANONYMOUS` for the lab (production would require an APIM front, a shared-secret header, or Entra-token validation — noted in the exercises but out of scope here).

## Notes

- **Env-var naming follows the AI-3026 MCP convention** — `FOUNDRY_PROJECT_ENDPOINT` + `FOUNDRY_MODEL`, matching MS Learn `mslearn-ai-agents`.
- **Model pin**: `gpt-5` version `2025-08-07` (GA on GlobalStandard in eastus2 per MS Learn 2026-08-23).
- **`requirements.txt` reference-only.** `mcp`, `fastmcp`, and `starlette` were added to the `python-ai` container specifically for MCP tool lessons; every listed package is already resolved.
- The MCP server has **no auth** on the local port and uses `AuthLevel.ANONYMOUS` on the Function App. Do NOT expose this pattern to a public production network without a reverse proxy + auth layer.
