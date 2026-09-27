"""Smoke test — introspect the FastMCP server without a real stdio client."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from server import mcp


async def main():
    # FastMCP exposes internal handlers via mcp._tool_manager and similar internal APIs
    # (subject to SDK version drift). Simplest smoke test: call the tool functions directly.
    print("Registered tools:")
    for name in dir(mcp):
        if name.startswith("_"): continue
    # Instead of introspection, just invoke known tool names if they exist.
    try:
        # FastMCP registers tools; try known names:
        for t in ("greet", "add", "lookup_customer_tier"):
            fn = None
            # The registered tools live in mcp._tool_manager._tools in current SDK versions.
            if hasattr(mcp, "_tool_manager") and hasattr(mcp._tool_manager, "_tools"):
                fn = mcp._tool_manager._tools.get(t)
                if fn is not None:
                    print(f"  ✓ {t}: registered")
                else:
                    print(f"  ✗ {t}: NOT registered (TODO not filled?)")
    except Exception as e:
        print(f"(Introspection unavailable in this SDK version: {e})")

    print("\nDirect function calls:")
    try:
        from server import greet, add, lookup_customer_tier
        print(f"  greet('Priya') = {greet('Priya')!r}")
        print(f"  add(2, 3) = {add(2, 3)}")
        print(f"  lookup_customer_tier('acme-corp') = {lookup_customer_tier('acme-corp')!r}")
    except ImportError as e:
        print(f"  Import failed (TODOs not filled): {e}")


if __name__ == "__main__":
    asyncio.run(main())
