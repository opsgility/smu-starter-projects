"""COMPLETE: in-process mock MCP-shape server for teaching the protocol.

Real MCP servers run as subprocesses and speak JSON-RPC over stdio.
This mock lives in-process for simplicity — same message SHAPE, no
subprocess plumbing.
"""

import json


class MockMCPServer:
    """Serves 3 tools (add, get_weather, list_orion_customers)."""

    def initialize(self, params: dict) -> dict:
        return {
            "protocolVersion": "2025-06-01",
            "serverInfo": {"name": "orion-mock-server", "version": "0.1.0"},
            "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
        }

    def tools_list(self, params: dict) -> dict:
        return {
            "tools": [
                {
                    "name": "add",
                    "description": "Add two numbers.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                        "required": ["a", "b"],
                    },
                },
                {
                    "name": "get_weather",
                    "description": "Get the current weather for a city.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                        "required": ["city"],
                    },
                },
                {
                    "name": "list_orion_customers",
                    "description": "List Orion Analytics customer IDs.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"tier_filter": {"type": "string",
                                                       "enum": ["Enterprise", "Pro", "Starter", "all"]}},
                        "required": [],
                    },
                },
            ]
        }

    def tools_call(self, params: dict) -> dict:
        name = params["name"]
        args = params.get("arguments", {})
        if name == "add":
            return {"content": [{"type": "text", "text": str(args["a"] + args["b"])}]}
        if name == "get_weather":
            return {"content": [{"type": "text",
                                 "text": json.dumps({"city": args["city"], "temp_f": 72, "conditions": "sunny"})}]}
        if name == "list_orion_customers":
            filt = args.get("tier_filter", "all")
            data = {"Enterprise": ["acme-corp", "orbit-metrics"],
                    "Pro": ["beta-labs", "quantum-data"],
                    "Starter": ["widget-inc"]}
            if filt == "all":
                out = [c for v in data.values() for c in v]
            else:
                out = data.get(filt, [])
            return {"content": [{"type": "text", "text": json.dumps({"customers": out})}]}
        return {"content": [{"type": "text", "text": f"unknown tool {name}"}], "isError": True}

    def dispatch(self, request: dict) -> dict:
        """JSON-RPC-style dispatch: {jsonrpc, id, method, params} → response dict."""
        method_map = {
            "initialize": self.initialize,
            "tools/list": self.tools_list,
            "tools/call": self.tools_call,
        }
        method = request.get("method")
        fn = method_map.get(method)
        if fn is None:
            return {"jsonrpc": "2.0", "id": request.get("id"),
                    "error": {"code": -32601, "message": f"method not found: {method}"}}
        try:
            result = fn(request.get("params") or {})
            return {"jsonrpc": "2.0", "id": request.get("id"), "result": result}
        except Exception as e:
            return {"jsonrpc": "2.0", "id": request.get("id"),
                    "error": {"code": -32000, "message": str(e)}}
