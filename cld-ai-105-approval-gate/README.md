# CLD-AI-105 L8 — MCP approval gate

Wrap the multi-server client from L6 with a Y/N approval prompt before every tool call. Implements the per-tool-call consent pattern.

## Files
- `.env.example`, `.gitignore`, `requirements.txt`, `verify_env.py`
- `mock_servers.py` — reused from L6.
- `approval_client.py` — wraps MultiMCPClient with a callable approval hook.
