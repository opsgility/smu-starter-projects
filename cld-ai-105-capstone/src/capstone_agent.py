"""Capstone: multi-server MCP + Claude agent for Orion triage."""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from orion_server import OrionServer
from runbook_server import RunbookServer


SERVERS = {"orion": OrionServer(), "runbook": RunbookServer()}


def _rpc(server_name, method, params=None, rid=[0]):
    rid[0] += 1
    r = SERVERS[server_name].dispatch({"jsonrpc":"2.0","id":rid[0],"method":method,"params":params or {}})
    if "error" in r: raise RuntimeError(r["error"])
    return r["result"]


def aggregate_anthropic_tools() -> tuple[list[dict], dict[str, str]]:
    """Return (anthropic_tools_list, tool_name_to_server_map)."""
    tools = []
    routing = {}
    for name in SERVERS:
        _rpc(name, "initialize")
        for t in _rpc(name, "tools/list")["tools"]:
            # Prefix tool name with server for disambiguation
            anthropic_name = f"{name}__{t['name']}"
            tools.append({
                "name": anthropic_name,
                "description": f"[{name}] {t['description']}",
                "input_schema": t["inputSchema"],
            })
            routing[anthropic_name] = (name, t["name"])
    return tools, routing


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    tools, routing = aggregate_anthropic_tools()
    print("Aggregated tools:")
    for t in tools:
        print(f"  {t['name']}: {t['description']}")

    user_prompt = ("Customer 'widget-inc' opened a refund ticket. Look up their status, "
                   "check the refund runbook, and recommend an action.")
    messages = [{"role":"user","content": user_prompt}]

    # TODO: agent loop. On each iteration:
    #   - call client.messages.create(model, max_tokens=1024, tools=tools, messages=messages)
    #   - append assistant reply to messages
    #   - if stop_reason=="end_turn", extract text and return
    #   - else for each tool_use block, look up routing[block.name] = (server, real_tool),
    #     call _rpc(server, "tools/call", {"name": real_tool, "arguments": dict(block.input)}),
    #     build tool_result blocks, append as one user message, continue
    #
    # HINT: same pattern as CLD-AI-103 L2 agent loop.
    for iteration in range(1, 10):
        resp = client.messages.create(model=model, max_tokens=1024, tools=tools, messages=messages)
        messages.append({"role":"assistant","content": resp.content})
        if resp.stop_reason == "end_turn":
            text = next((b.text for b in resp.content if b.type == "text"), "")
            print(f"\n=== FINAL ({iteration} iterations) ===\n{text}")
            return 0
        tool_results = []
        for block in resp.content:
            if block.type != "tool_use": continue
            server, real_tool = routing[block.name]
            print(f"  iter {iteration}: {block.name} → {server}::{real_tool}({dict(block.input)})")
            r = _rpc(server, "tools/call", {"name": real_tool, "arguments": dict(block.input)})
            tool_results.append({"type":"tool_result","tool_use_id": block.id, "content": r["content"][0]["text"]})
        messages.append({"role":"user","content": tool_results})

    print("max iter exceeded"); return 1


if __name__ == "__main__":
    sys.exit(main())
