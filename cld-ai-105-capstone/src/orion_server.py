import json

DB = {"acme-corp":{"tier":"Enterprise","status":"active"},
      "widget-inc":{"tier":"Starter","status":"suspended"}}


class OrionServer:
    def dispatch(self, req):
        rid = req.get("id"); m = req.get("method"); p = req.get("params") or {}
        if m == "initialize":
            return {"jsonrpc":"2.0","id":rid,"result":{"serverInfo":{"name":"orion"},"capabilities":{"tools":{}}}}
        if m == "tools/list":
            return {"jsonrpc":"2.0","id":rid,"result":{"tools":[
                {"name":"lookup_customer","description":"Look up an Orion customer by id.",
                 "inputSchema":{"type":"object","properties":{"customer_id":{"type":"string"}},"required":["customer_id"]}, "risk":"read"},
            ]}}
        if m == "tools/call" and p["name"] == "lookup_customer":
            cid = p["arguments"]["customer_id"]
            return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text": json.dumps(DB.get(cid, {"error":"not found"}))}]}}
        return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"unknown"}}
