"""Same shape as L6 mock_servers — orion (read-only) + filesystem (dangerous write)."""

import json


class OrionServer:
    def dispatch(self, req):
        rid = req.get("id"); m = req.get("method"); p = req.get("params") or {}
        if m == "initialize":
            return {"jsonrpc":"2.0","id":rid,"result":{"protocolVersion":"2025-06-01","serverInfo":{"name":"orion"},"capabilities":{"tools":{}}}}
        if m == "tools/list":
            return {"jsonrpc":"2.0","id":rid,"result":{"tools":[
                {"name":"lookup_customer","description":"Read-only customer lookup.",
                 "inputSchema":{"type":"object","properties":{"customer_id":{"type":"string"}},"required":["customer_id"]},
                 "risk":"read"},
            ]}}
        if m == "tools/call" and p["name"] == "lookup_customer":
            return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text": json.dumps({"cid": p["arguments"]["customer_id"], "tier":"Pro"})}]}}
        return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"unknown"}}


class FilesystemServer:
    def dispatch(self, req):
        rid = req.get("id"); m = req.get("method"); p = req.get("params") or {}
        if m == "initialize":
            return {"jsonrpc":"2.0","id":rid,"result":{"protocolVersion":"2025-06-01","serverInfo":{"name":"filesystem"},"capabilities":{"tools":{}}}}
        if m == "tools/list":
            return {"jsonrpc":"2.0","id":rid,"result":{"tools":[
                {"name":"read_file","description":"Read a file.",
                 "inputSchema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}, "risk":"read"},
                {"name":"delete_file","description":"DANGER: delete a file.",
                 "inputSchema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}, "risk":"destructive"},
            ]}}
        if m == "tools/call":
            if p["name"] == "read_file":
                return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text": f"(mock file contents at {p['arguments']['path']})"}]}}
            if p["name"] == "delete_file":
                return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text": f"deleted {p['arguments']['path']}"}]}}
        return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"unknown"}}
