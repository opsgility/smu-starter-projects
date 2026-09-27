# CLD-AI-106 L2 — Your first FastMCP server

Uses the official `mcp` Python SDK. Ships an in-process test harness so you can verify server behavior WITHOUT running stdio subprocess plumbing (the SDK's real transport is stdio for local; this lab includes a `test_server.py` that calls the FastMCP server's dispatch layer directly for pedagogical simplicity).

## Files
- `server.py` — Exercise 2: TODO add 3 tools with FastMCP decorators
- `test_server.py` — smoke test via in-process dispatch
