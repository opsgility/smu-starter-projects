"""Adapter that exposes the fastmcp `mcp` object as a Starlette ASGI app.

The Azure Functions Python worker's `AsgiMiddleware` forwards every request under
the `mcp/{*path}` route into this app. fastmcp already ships a streamable-HTTP
Starlette app internally; we just fetch it and add a health endpoint the Function
route can also serve locally.
"""
from __future__ import annotations

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from .ridgevault_tools import mcp


async def _healthz(_request):
    return JSONResponse({"status": "ok", "service": "ridgevault-mcp-tools"})


def build_asgi_app() -> Starlette:
    """Return the composed Starlette app the Function App mounts under /api/mcp."""
    # fastmcp.http_app() returns a full Starlette streamable-HTTP application.
    # We mount it at the root so a request to /api/mcp/... reaches /... inside
    # fastmcp (the Function App strips the /api/mcp prefix via its route).
    mcp_app = mcp.http_app(path="/")

    return Starlette(
        routes=[
            Route("/healthz", _healthz, methods=["GET"]),
            Mount("/", app=mcp_app),
        ],
        lifespan=mcp_app.lifespan,
    )
