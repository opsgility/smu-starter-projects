# CLD-AI-105 Lesson 2 — Connect to an MCP server from Python

First CLD-AI-105 hands-on. Build a minimal MCP client in Python that connects to a simple in-process MCP-shape server (JSON-RPC vocabulary), discovers its tools, and calls them. Real production clients use the `mcp` PyPI package; this exercise uses an in-process shim so students focus on the protocol shape without shell/subprocess complications.

## Files
```
cld-ai-105-mcp-client/
  README.md, .env.example, .gitignore, requirements.txt
  src/
    verify_env.py
    mock_mcp_server.py    # COMPLETE: in-process class simulating MCP JSON-RPC vocabulary.
    mcp_client.py         # Exercise 2 — TODO: discover + call the mock server.
    claude_with_mcp.py    # Exercise 3 — expose MCP tools to Claude via tool_use.
```
