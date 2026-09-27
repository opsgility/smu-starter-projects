"""Exercise 2 — fill in list_resources/read_resource/list_prompts/get_prompt.

Run: `python src/client.py`
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mock_server import MockMCPServer


class MCPClient:
    def __init__(self, server): self.server = server; self._id = 0

    def _rpc(self, method, params=None):
        self._id += 1
        r = self.server.dispatch({"jsonrpc":"2.0","id":self._id,"method":method,"params":params or {}})
        if "error" in r: raise RuntimeError(r["error"])
        return r["result"]

    def initialize(self): return self._rpc("initialize", {"protocolVersion":"2025-06-01"})

    def list_tools(self): return self._rpc("tools/list")["tools"]
    def call_tool(self, name, args): return self._rpc("tools/call", {"name": name, "arguments": args})["content"][0]["text"]

    def list_resources(self):
        # TODO: return self._rpc("resources/list")["resources"]
        raise NotImplementedError("TODO: list_resources")

    def read_resource(self, uri):
        # TODO: return self._rpc("resources/read", {"uri": uri})["contents"][0]["text"]
        raise NotImplementedError("TODO: read_resource")

    def list_prompts(self):
        # TODO: return self._rpc("prompts/list")["prompts"]
        raise NotImplementedError("TODO: list_prompts")

    def get_prompt(self, name, arguments):
        # TODO: return self._rpc("prompts/get", {"name": name, "arguments": arguments})["messages"][0]["content"]["text"]
        raise NotImplementedError("TODO: get_prompt")


def main():
    c = MCPClient(MockMCPServer())
    c.initialize()
    print("tools:", [t["name"] for t in c.list_tools()])
    print("resources:", [r["uri"] for r in c.list_resources()])
    print("sla read:", c.read_resource("orion://runbook/sla")[:60])
    print("prompts:", [p["name"] for p in c.list_prompts()])
    print("prompt text:", c.get_prompt("review-ticket", {"ticket_text": "test ticket"}))
    return 0


if __name__ == "__main__": sys.exit(main())
