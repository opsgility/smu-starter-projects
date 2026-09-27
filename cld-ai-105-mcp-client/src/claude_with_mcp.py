"""Exercise 3 — expose MCP tools to Claude via the tool_use loop from CLD-AI-103."""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mock_mcp_server import MockMCPServer
from mcp_client import MCPClient


def mcp_tool_to_anthropic_schema(mcp_tool: dict) -> dict:
    """Translate MCP tool schema to Anthropic Messages API tool schema."""
    return {
        "name": mcp_tool["name"],
        "description": mcp_tool["description"],
        "input_schema": mcp_tool["inputSchema"],
    }


def main() -> int:
    load_dotenv()
    client_claude = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    mcp = MCPClient(MockMCPServer())
    mcp.initialize()
    mcp_tools = mcp.list_tools()

    anthropic_tools = [mcp_tool_to_anthropic_schema(t) for t in mcp_tools]

    prompt = ("Add 17 and 25, then get the weather for Portland, then list the Enterprise "
              "Orion customers. Report the results.")
    messages = [{"role": "user", "content": prompt}]

    for iteration in range(1, 10):
        resp = client_claude.messages.create(
            model=model, max_tokens=1024,
            tools=anthropic_tools,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason == "end_turn":
            text = next((b.text for b in resp.content if b.type == "text"), "")
            print(f"\n=== FINAL ANSWER (after {iteration} iterations) ===\n{text}")
            return 0

        tool_results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue
            print(f"  iter {iteration}: Claude calling MCP tool {block.name}({block.input})")
            mcp_result = mcp.call_tool(block.name, dict(block.input))
            tool_results.append({
                "type": "tool_result", "tool_use_id": block.id, "content": mcp_result,
            })
        messages.append({"role": "user", "content": tool_results})

    print("max iterations exceeded"); return 1


if __name__ == "__main__":
    sys.exit(main())
