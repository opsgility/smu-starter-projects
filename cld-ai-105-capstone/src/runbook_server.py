RUNBOOK = {
    "sla": "Sev-1: 15-min response, 4-hour resolution. Sev-2: 1h/24h. Sev-3: 4h/72h.",
    "refund": "Refunds only on active accounts. Suspended/cancelled accounts must be escalated to CSM.",
    "escalation": "Escalate to on-call CSM if account status is suspended or cancelled.",
}


class RunbookServer:
    def dispatch(self, req):
        rid = req.get("id"); m = req.get("method"); p = req.get("params") or {}
        if m == "initialize":
            return {"jsonrpc":"2.0","id":rid,"result":{"serverInfo":{"name":"runbook"},"capabilities":{"tools":{}}}}
        if m == "tools/list":
            return {"jsonrpc":"2.0","id":rid,"result":{"tools":[
                {"name":"lookup_runbook","description":"Fetch a runbook section by name (sla|refund|escalation).",
                 "inputSchema":{"type":"object","properties":{"name":{"type":"string","enum":list(RUNBOOK.keys())}},"required":["name"]}, "risk":"read"},
            ]}}
        if m == "tools/call" and p["name"] == "lookup_runbook":
            n = p["arguments"]["name"]
            return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text": RUNBOOK.get(n, "(unknown runbook)")}]}}
        return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"unknown"}}
