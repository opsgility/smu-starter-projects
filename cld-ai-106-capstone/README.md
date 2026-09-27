# CLD-AI-106 L10 — Capstone: complete Orion MCP server (packaged)

Ship a packaged MCP server exposing tools + resources + prompts for Orion Analytics. Test end-to-end via the L2-style in-process harness.

## Files
- `pyproject.toml` — package config with console-script entry point.
- `src/orion_mcp/__init__.py`
- `src/orion_mcp/server.py` — 3 tools + 2 resources + 1 prompt.
- `src/orion_mcp/__main__.py` — entry point.
- `test_e2e.py` — smoke test.
