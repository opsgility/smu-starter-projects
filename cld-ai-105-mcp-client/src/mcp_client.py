"""Exercise 2 — build an MCP client that discovers + calls tools on the mock server.

Fill in the TWO TODOs to (1) discover tools via tools/list and (2) call a
specific tool via tools/call. The dispatch shape is JSON-RPC.

Run standalone: `python src/mcp_client.py`
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mock_mcp_server import MockMCPServer


class MCPClient:
    def __init__(self, server: MockMCPServer):
        self.server = server
        self._id = 0

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    def _rpc(self, method: str, params: dict = None) -> dict:
        """Send one JSON-RPC request; return response dict."""
        request = {"jsonrpc": "2.0", "id": self._next_id(), "method": method, "params": params or {}}
        response = self.server.dispatch(request)
        if "error" in response:
            raise RuntimeError(f"MCP error: {response['error']}")
        return response["result"]

    def initialize(self) -> dict:
        return self._rpc("initialize", {"protocolVersion": "2025-06-01"})

    def list_tools(self) -> list[dict]:
        # TODO 1: call tools/list via self._rpc and return the "tools" list.
        # HINT:
        #   result = self._rpc("tools/list")
        #   return result["tools"]
        raise NotImplementedError("TODO 1: implement list_tools")

    def call_tool(self, name: str, arguments: dict) -> str:
        # TODO 2: call tools/call via self._rpc with {"name": name, "arguments": arguments}.
        # Extract the text from result["content"][0]["text"] and return it.
        # HINT:
        #   result = self._rpc("tools/call", {"name": name, "arguments": arguments})
        #   return result["content"][0]["text"]
        raise NotImplementedError("TODO 2: implement call_tool")


def main() -> int:
    client = MCPClient(MockMCPServer())
    print(f"init: {client.initialize()}")
    tools = client.list_tools()
    print(f"\ntools discovered: {len(tools)}")
    for t in tools:
        print(f"  {t['name']}: {t['description']}")

    print("\ncalling add(2, 3):")
    print(f"  result: {client.call_tool('add', {'a': 2, 'b': 3})}")

    print("\ncalling get_weather('Seattle'):")
    print(f"  result: {client.call_tool('get_weather', {'city': 'Seattle'})}")

    print("\ncalling list_orion_customers(tier_filter='Enterprise'):")
    print(f"  result: {client.call_tool('list_orion_customers', {'tier_filter': 'Enterprise'})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
