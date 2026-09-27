"""Two mock MCP-shape servers with dispatch()."""

import json


def _rpc_response(req_id, result=None, error=None):
    if error is not None:
        return {"jsonrpc":"2.0","id":req_id,"error":error}
    return {"jsonrpc":"2.0","id":req_id,"result":result}


class OrionServer:
    def dispatch(self, req):
        rid = req.get("id"); m = req.get("method"); p = req.get("params") or {}
        if m == "initialize":
            return _rpc_response(rid, {"protocolVersion":"2025-06-01","serverInfo":{"name":"orion","version":"1"},"capabilities":{"tools":{}}})
        if m == "tools/list":
            return _rpc_response(rid, {"tools": [
                {"name":"lookup_customer","description":"Look up Orion customer by id.",
                 "inputSchema":{"type":"object","properties":{"customer_id":{"type":"string"}},"required":["customer_id"]}},
            ]})
        if m == "tools/call":
            if p["name"] == "lookup_customer":
                db = {"acme-corp":{"tier":"Enterprise"}, "widget-inc":{"tier":"Starter","status":"suspended"}}
                cid = p["arguments"]["customer_id"]
                return _rpc_response(rid, {"content":[{"type":"text","text": json.dumps(db.get(cid, {"error":"not found"}))}]})
        return _rpc_response(rid, error={"code":-32601,"message":f"unknown {m}"})


class WeatherServer:
    def dispatch(self, req):
        rid = req.get("id"); m = req.get("method"); p = req.get("params") or {}
        if m == "initialize":
            return _rpc_response(rid, {"protocolVersion":"2025-06-01","serverInfo":{"name":"weather","version":"1"},"capabilities":{"tools":{}}})
        if m == "tools/list":
            return _rpc_response(rid, {"tools": [
                {"name":"forecast","description":"Get weather forecast for a city.",
                 "inputSchema":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}},
            ]})
        if m == "tools/call":
            if p["name"] == "forecast":
                return _rpc_response(rid, {"content":[{"type":"text","text": json.dumps({"city": p["arguments"]["city"], "temp_f": 68, "sky":"cloudy"})}]})
        return _rpc_response(rid, error={"code":-32601,"message":f"unknown {m}"})
