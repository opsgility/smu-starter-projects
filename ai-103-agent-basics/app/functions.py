"""Function tools for the Summitline Outfitters concierge agent.

Each callable in :data:`USER_FUNCTIONS` is registered with
:class:`azure.ai.agents.models.FunctionTool`, which parses the Sphinx-style
``:param:`` lines in each docstring to generate the JSON tool schema at
runtime. **Do not remove or reformat** the ``:param:`` lines — the FunctionTool
schema builder depends on them.
"""
from __future__ import annotations

import ast
import operator
from typing import Any, Dict, Set


# ---------------------------------------------------------------------------
# get_weather
# ---------------------------------------------------------------------------

# Mock weather data keyed on the cities Summitline ships to most often.
_WEATHER_TABLE: Dict[str, Dict[str, Any]] = {
    "bend": {"temperature_f": 64, "condition": "clear"},
    "redmond": {"temperature_f": 58, "condition": "partly cloudy"},
    "seattle": {"temperature_f": 55, "condition": "light rain"},
    "portland": {"temperature_f": 61, "condition": "overcast"},
    "boise": {"temperature_f": 72, "condition": "sunny"},
    "denver": {"temperature_f": 68, "condition": "sunny"},
    "salt lake city": {"temperature_f": 70, "condition": "clear"},
}


def get_weather(city: str) -> Dict[str, Any]:
    """Return the current weather conditions for a Summitline ship-to city.

    Used by the concierge to advise customers on shipping and trail-ready
    gear. Returns mocked data so the lab runs without an external API key.

    :param city: The city to look up. Case-insensitive. Example: ``"Bend"``.
    :return: A dict with ``city``, ``temperature_f``, and ``condition``.
    """
    key = (city or "").strip().lower()
    record = _WEATHER_TABLE.get(key)
    if record is None:
        return {
            "city": city,
            "temperature_f": 62,
            "condition": "clear",
            "note": "No local reading — returned a seasonal default.",
        }
    return {"city": city, **record}


# ---------------------------------------------------------------------------
# calculate
# ---------------------------------------------------------------------------

# Allow a safe subset of Python arithmetic operators — no name lookups, no
# function calls, no attribute access. Protects against arbitrary code.
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        return _ALLOWED_BINOPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARYOPS:
        return _ALLOWED_UNARYOPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Only numeric expressions with + - * / // % ** are allowed.")


def calculate(expression: str) -> Dict[str, Any]:
    """Evaluate a numeric expression for bulk-order math and shipping totals.

    Supports the operators ``+``, ``-``, ``*``, ``/``, ``//``, ``%``, ``**``
    and parenthesised sub-expressions. Rejects any non-arithmetic input.

    :param expression: The arithmetic expression to evaluate. Example: ``"47 * 12"``.
    :return: A dict with the original ``expression`` and the numeric ``result``.
    """
    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree)
    except (SyntaxError, ValueError, ZeroDivisionError) as exc:
        return {"expression": expression, "error": str(exc)}
    return {"expression": expression, "result": result}


# ---------------------------------------------------------------------------
# lookup_inventory
# ---------------------------------------------------------------------------

# Mock SKU catalog — the three SKUs the exercise test conversation references
# (NW-SL-001, NW-SL-002) plus a third entry for multi-tool demos.
_INVENTORY_TABLE: Dict[str, Dict[str, Any]] = {
    "NW-SL-001": {
        "name": "Summitline Alpine Trekker 45L Pack",
        "in_stock": 42,
        "warehouse": "Bend, OR",
        "price_usd": 189.00,
    },
    "NW-SL-002": {
        "name": "Summitline Ridgeline Softshell Jacket",
        "in_stock": 17,
        "warehouse": "Redmond, OR",
        "price_usd": 149.00,
    },
    "NW-SL-003": {
        "name": "Summitline Cascade 3-Season Tent (2P)",
        "in_stock": 0,
        "warehouse": "Bend, OR",
        "price_usd": 329.00,
        "note": "Back-ordered — next shipment in 14 days.",
    },
}


def lookup_inventory(sku: str) -> Dict[str, Any]:
    """Return current stock information for a Summitline SKU.

    All Summitline SKUs follow the pattern ``NW-SL-###``. Unknown SKUs return
    a structured "not found" response so the model can still answer the user.

    :param sku: The Summitline SKU to look up. Example: ``"NW-SL-001"``.
    :return: A dict with ``sku``, product ``name``, ``in_stock`` count,
             originating ``warehouse``, and ``price_usd`` — or an ``error``
             field when the SKU is not in the catalog.
    """
    key = (sku or "").strip().upper()
    record = _INVENTORY_TABLE.get(key)
    if record is None:
        return {"sku": sku, "error": f"No Summitline SKU matches '{sku}'."}
    return {"sku": key, **record}


# The set of callables FunctionTool will convert into tool definitions.
# Tests assert membership against these exact references — keep the names.
USER_FUNCTIONS: Set[Any] = {get_weather, calculate, lookup_inventory}
