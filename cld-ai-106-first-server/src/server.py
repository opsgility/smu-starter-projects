"""Exercise 2 — FastMCP server exposing 3 tools.

Fill in 3 TODO tools using the FastMCP decorator + type hints.

Run standalone (stdio transport, exits when stdin closes):
  python src/server.py

Or test via the harness:
  python src/test_server.py
"""

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("ERROR: 'mcp' package not installed. Run: pip install mcp")
    raise


mcp = FastMCP("orion-server")


# TODO 1: implement 'greet' tool that takes a `name` string and returns a greeting.
# HINT:
#   @mcp.tool()
#   def greet(name: str) -> str:
#       """Return a friendly greeting."""
#       return f"Hello, {name}!"


# TODO 2: implement 'add' tool that takes two numbers and returns their sum.
# HINT:
#   @mcp.tool()
#   def add(a: float, b: float) -> float:
#       """Add two numbers."""
#       return a + b


# TODO 3: implement 'lookup_customer_tier' tool that takes customer_id and returns tier.
# HINT:
#   TIERS = {"acme-corp":"Enterprise","widget-inc":"Starter","beta-labs":"Pro"}
#   @mcp.tool()
#   def lookup_customer_tier(customer_id: str) -> str:
#       """Look up the subscription tier for a customer."""
#       return TIERS.get(customer_id, "unknown")


if __name__ == "__main__":
    mcp.run()  # stdio transport
