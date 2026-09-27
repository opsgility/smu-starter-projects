"""Exercise — load config, connect to all servers, aggregate tools, route calls."""

import importlib
import json
import sys
from pathlib import Path


class MultiMCPClient:
    def __init__(self, config_path: Path):
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
        self.servers = {}
        for name, s in cfg["servers"].items():
            mod = importlib.import_module(s["module"])
            klass = getattr(mod, s["class"])
            self.servers[name] = klass()
        self._id = 0

    def _next_id(self):
        self._id += 1
        return self._id

    def _rpc(self, server_name, method, params=None):
        req = {"jsonrpc":"2.0","id":self._next_id(),"method":method,"params":params or {}}
        r = self.servers[server_name].dispatch(req)
        if "error" in r: raise RuntimeError(r["error"])
        return r["result"]

    def initialize_all(self):
        return {n: self._rpc(n, "initialize") for n in self.servers}

    def aggregate_tools(self) -> list[dict]:
        """TODO: return list of {'server': name, 'schema': mcp_tool_schema} across ALL servers.
        HINT:
          out = []
          for name in self.servers:
              tools = self._rpc(name, "tools/list")["tools"]
              for t in tools:
                  out.append({"server": name, "schema": t})
          return out
        """
        raise NotImplementedError("TODO: aggregate_tools")

    def call_tool(self, server_name: str, tool_name: str, arguments: dict) -> str:
        """TODO: route the tools/call to the right server.
        HINT:
          r = self._rpc(server_name, "tools/call", {"name": tool_name, "arguments": arguments})
          return r["content"][0]["text"]
        """
        raise NotImplementedError("TODO: call_tool")


def main():
    cfg_path = Path(__file__).resolve().parent.parent / "mcp_config.json"
    # We register the src/ dir on sys.path so importlib finds mock_servers
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    c = MultiMCPClient(cfg_path)
    print("init:", c.initialize_all())
    tools = c.aggregate_tools()
    print("\naggregated tools:")
    for t in tools:
        print(f"  {t['server']}::{t['schema']['name']}  — {t['schema']['description']}")
    print("\nlookup acme-corp:", c.call_tool("orion", "lookup_customer", {"customer_id": "acme-corp"}))
    print("weather Seattle:", c.call_tool("weather", "forecast", {"city": "Seattle"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
