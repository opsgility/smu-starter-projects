"""COMPLETE: MockMCPServer with tools + resources + prompts."""

import json


RESOURCES_DB = {
    "orion://runbook/sla": "Sev-1 SLA: 15 min response, 4h resolution.\nSev-2 SLA: 1h/24h.",
    "orion://policy/refund": "Full refund within 30 days. Prorated after. None on suspended.",
    "orion://config/current": '{"env":"prod","region":"us-east-1","version":"2026.9.1"}',
}

PROMPTS_DB = {
    "review-ticket": {
        "description": "Review a support ticket and recommend an action.",
        "arguments": [{"name": "ticket_text", "required": True}],
        "template": "Review this ticket:\n\n{ticket_text}\n\nRecommend a category and next step.",
    },
    "summarize-week": {
        "description": "Summarize a week of support ticket activity.",
        "arguments": [{"name": "period", "required": True}],
        "template": "Summarize Orion support activity for period {period}.",
    },
}


class MockMCPServer:
    def initialize(self, params):
        return {"protocolVersion": "2025-06-01",
                "serverInfo": {"name": "orion-multi-server", "version": "0.2.0"},
                "capabilities": {"tools": {}, "resources": {}, "prompts": {}}}

    def tools_list(self, params):
        return {"tools": [
            {"name": "add", "description": "Add two numbers.",
             "inputSchema": {"type":"object","properties":{"a":{"type":"number"},"b":{"type":"number"}},"required":["a","b"]}},
        ]}

    def tools_call(self, params):
        args = params.get("arguments", {})
        if params["name"] == "add":
            return {"content": [{"type": "text", "text": str(args["a"] + args["b"])}]}
        return {"content": [{"type":"text","text":"unknown"}], "isError": True}

    def resources_list(self, params):
        return {"resources": [
            {"uri": uri, "name": uri.split("/")[-1], "mimeType": "text/plain"}
            for uri in RESOURCES_DB
        ]}

    def resources_read(self, params):
        uri = params["uri"]
        if uri not in RESOURCES_DB:
            raise KeyError(f"resource not found: {uri}")
        return {"contents": [{"uri": uri, "mimeType": "text/plain", "text": RESOURCES_DB[uri]}]}

    def prompts_list(self, params):
        return {"prompts": [
            {"name": name, "description": p["description"], "arguments": p["arguments"]}
            for name, p in PROMPTS_DB.items()
        ]}

    def prompts_get(self, params):
        name = params["name"]
        args = params.get("arguments", {})
        p = PROMPTS_DB[name]
        text = p["template"].format(**args)
        return {"description": p["description"],
                "messages": [{"role": "user", "content": {"type": "text", "text": text}}]}

    def dispatch(self, req):
        m = {"initialize": self.initialize, "tools/list": self.tools_list, "tools/call": self.tools_call,
             "resources/list": self.resources_list, "resources/read": self.resources_read,
             "prompts/list": self.prompts_list, "prompts/get": self.prompts_get}
        method = req.get("method"); fn = m.get(method)
        if fn is None:
            return {"jsonrpc":"2.0","id":req.get("id"),"error":{"code":-32601,"message":f"unknown {method}"}}
        try:
            return {"jsonrpc":"2.0","id":req.get("id"),"result": fn(req.get("params") or {})}
        except Exception as e:
            return {"jsonrpc":"2.0","id":req.get("id"),"error":{"code":-32000,"message":str(e)}}
