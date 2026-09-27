# CLD-AI-105 L6 — Multi-server MCP client with config file

Client loads server configs from mcp_config.json and connects to multiple in-process mock servers. Tools are aggregated across servers; calls are routed by name prefix.

## Files
- `mcp_config.json` — declares 2 servers.
- `mock_servers.py` — 2 mock server classes (orion + weather).
- `multi_client.py` — TODO: load config + connect + aggregate + route.
