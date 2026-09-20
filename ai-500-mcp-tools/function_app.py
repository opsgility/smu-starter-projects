"""Azure Functions HTTP entry that hosts the Ridgevault fastmcp server.

Exposes:
  GET  /api/mcp/healthz  -> liveness probe (no MCP handshake required)
  ANY  /api/mcp/{*path}  -> full MCP streamable-HTTP surface (JSON-RPC + SSE)

The Function App runs on Flex Consumption (Linux, Python 3.11). Because Flex
Consumption's deployment path stores the zipped payload in a managed-identity-
authenticated blob container, we do NOT set WEBSITE_RUN_FROM_PACKAGE — the
runtime reads app files directly from the mount.

AuthLevel.ANONYMOUS is deliberate for this lab. A production deployment would
front the endpoint with APIM or a shared-secret header (see README Notes).
"""
from __future__ import annotations

import azure.functions as func

from src.mcp_server.function_wrapper import build_asgi_app


# Build the Starlette ASGI app once at cold-start; every request reuses it.
_asgi_app = build_asgi_app()

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="mcp/healthz", methods=["GET"])
def healthz(req: func.HttpRequest) -> func.HttpResponse:
    """Liveness probe. Returns {"status": "ok"} — used by the agent runtime
    to verify the tool endpoint is reachable before opening the MCP handshake.
    """
    return func.HttpResponse(
        body='{"status":"ok","service":"ridgevault-mcp-tools"}',
        status_code=200,
        mimetype="application/json",
    )


@app.route(
    route="mcp/{*path}",
    methods=["GET", "POST", "OPTIONS"],
)
async def mcp_proxy(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Route every non-healthz /api/mcp/* request into the fastmcp Starlette app."""
    return await func.AsgiMiddleware(_asgi_app).handle_async(req, context)
