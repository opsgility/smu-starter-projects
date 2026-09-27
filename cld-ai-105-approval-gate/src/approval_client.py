"""Exercise — wrap MCP client with per-tool-call approval hook.

Fill the TODO to prompt approval before every tools/call.
Auto-approve tools whose 'risk' is 'read'; prompt for anything else.

Run: `python src/approval_client.py`
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mock_servers import OrionServer, FilesystemServer


class ApprovalMCPClient:
    def __init__(self):
        self.servers = {"orion": OrionServer(), "filesystem": FilesystemServer()}
        self.tools_cache: dict[tuple[str, str], dict] = {}
        self._id = 0
        self._auto_approve_risks = {"read"}
        # Simulated user answers for automated testing. When empty, use input().
        self.simulated_answers: list[str] = []

    def _rpc(self, srv, method, params=None):
        self._id += 1
        r = self.servers[srv].dispatch({"jsonrpc":"2.0","id":self._id,"method":method,"params":params or {}})
        if "error" in r: raise RuntimeError(r["error"])
        return r["result"]

    def discover(self):
        for name in self.servers:
            self._rpc(name, "initialize")
            for t in self._rpc(name, "tools/list")["tools"]:
                self.tools_cache[(name, t["name"])] = t

    def _ask_approval(self, server: str, tool_name: str, args: dict, risk: str) -> bool:
        if risk in self._auto_approve_risks:
            print(f"[auto-approved {risk}] {server}::{tool_name}({args})")
            return True
        prompt = f"\n>>> APPROVE {server}::{tool_name}({args}) [risk={risk}]? (y/n): "
        if self.simulated_answers:
            ans = self.simulated_answers.pop(0)
            print(f"{prompt}{ans}  (simulated)")
        else:
            ans = input(prompt).strip().lower()
        return ans == "y"

    def call_tool(self, server: str, tool_name: str, args: dict) -> str:
        # TODO: fetch tool metadata from tools_cache, extract 'risk' (default "unknown"),
        # call _ask_approval; if approved, dispatch tools/call; if not, return "(denied)".
        # HINT:
        #   tool = self.tools_cache.get((server, tool_name))
        #   risk = tool.get("risk", "unknown") if tool else "unknown"
        #   if not self._ask_approval(server, tool_name, args, risk):
        #       return "(denied by user)"
        #   result = self._rpc(server, "tools/call", {"name": tool_name, "arguments": args})
        #   return result["content"][0]["text"]
        raise NotImplementedError("TODO: implement call_tool with approval gate")


def main():
    c = ApprovalMCPClient()
    c.discover()
    print("tools discovered:", list(c.tools_cache.keys()))

    # Simulated user says y to read_file, n to delete_file
    c.simulated_answers = ["y", "n"]

    print("\n--- 1. lookup (read, auto-approved) ---")
    print(c.call_tool("orion", "lookup_customer", {"customer_id": "acme-corp"}))

    print("\n--- 2. read_file (unknown risk — user says y) ---")
    print(c.call_tool("filesystem", "read_file", {"path": "/tmp/readme.md"}))

    print("\n--- 3. delete_file (destructive — user says n) ---")
    print(c.call_tool("filesystem", "delete_file", {"path": "/tmp/important.txt"}))

    return 0


if __name__ == "__main__":
    sys.exit(main())
