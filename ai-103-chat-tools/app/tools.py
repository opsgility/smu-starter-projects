"""Tool definitions for the Summitline Outfitters chat assistant.

This module exports two things the `/chat` endpoint consumes:

* ``TOOL_SCHEMAS`` — the list of function-tool definitions passed to
  ``client.responses.create(tools=...)``. These use the OpenAI **Responses
  API** flat shape where ``type``, ``name``, ``description``, and
  ``parameters`` are top-level keys (no inner ``function:`` wrapper — that
  nested shape is for the legacy ``chat.completions`` API).

* ``DISPATCH`` — a ``{name: callable}`` map the main-loop uses to execute
  whichever Python function the model asks for.

Students do NOT modify this file — the exercise keeps the scope focused
on the tool-call loop itself in ``app/main.py``.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List


# ---------------------------------------------------------------------------
# Python implementations of the three tools
# ---------------------------------------------------------------------------

# A very small fake weather database. In a real app this would hit a REST API.
_WEATHER: Dict[str, Dict[str, Any]] = {
    "seattle": {"temp_f": 72, "condition": "sunny"},
    "portland": {"temp_f": 68, "condition": "overcast"},
    "denver": {"temp_f": 81, "condition": "clear"},
    "boulder": {"temp_f": 79, "condition": "partly cloudy"},
    "boston": {"temp_f": 64, "condition": "rain"},
    "austin": {"temp_f": 94, "condition": "hot"},
}

# A fake Summitline Outfitters inventory catalog. The SKU `SMT-HIKE-TENT-02`
# is the one referenced in the exercises and test_client.py.
_INVENTORY: Dict[str, Dict[str, Any]] = {
    "SMT-HIKE-TENT-02": {
        "name": "Summitline Ridgeline 2P Tent",
        "on_hand": 42,
        "warehouse": "Denver-DC",
        "price_usd": 289.00,
    },
    "SMT-HIKE-PACK-15": {
        "name": "Summitline Talus 55L Pack",
        "on_hand": 18,
        "warehouse": "Denver-DC",
        "price_usd": 219.00,
    },
    "SMT-CAMP-STOVE-01": {
        "name": "Summitline Backcountry Stove",
        "on_hand": 7,
        "warehouse": "Portland-DC",
        "price_usd": 79.00,
    },
}


def get_weather(city: str) -> Dict[str, Any]:
    """Return the current weather for a city (mock data)."""
    record = _WEATHER.get(city.strip().lower())
    if record is None:
        return {"city": city, "error": "unknown city"}
    return {
        "city": city,
        "temp_f": record["temp_f"],
        "condition": record["condition"],
    }


def calculate(expression: str) -> Dict[str, Any]:
    """Evaluate a simple arithmetic expression and return the numeric result.

    Only digits, whitespace, decimal points, parentheses, and the four
    basic operators are allowed — anything else returns an error so the
    model cannot trick the tool into executing arbitrary Python.
    """
    allowed = set("0123456789+-*/(). ")
    if not expression or any(ch not in allowed for ch in expression):
        return {"expression": expression, "error": "unsupported characters"}
    try:
        # eval is safe here because we've restricted the character set to
        # arithmetic only; there is no access to names, builtins, or calls.
        value = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
    except Exception as exc:  # pragma: no cover - defensive
        return {"expression": expression, "error": str(exc)}
    return {"expression": expression, "result": value}


def lookup_inventory(sku: str) -> Dict[str, Any]:
    """Return the on-hand count and metadata for a Summitline SKU."""
    record = _INVENTORY.get(sku.strip().upper())
    if record is None:
        return {"sku": sku, "error": "sku not found"}
    return {
        "sku": sku.strip().upper(),
        "name": record["name"],
        "on_hand": record["on_hand"],
        "warehouse": record["warehouse"],
        "price_usd": record["price_usd"],
    }


# ---------------------------------------------------------------------------
# Responses-API tool schemas (FLAT shape — no inner `function:` wrapper)
# ---------------------------------------------------------------------------

TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "name": "get_weather",
        "description": (
            "Get the current weather (temperature in Fahrenheit and a short "
            "condition label) for a city. Use this whenever a Summitline "
            "staffer or customer asks about outdoor conditions."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g. 'Seattle' or 'Denver'.",
                }
            },
            "required": ["city"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "calculate",
        "description": (
            "Evaluate a simple arithmetic expression (addition, subtraction, "
            "multiplication, division, parentheses). Use this for any math "
            "the user asks about — discount calculations, totals, ratios, "
            "etc. Do NOT pass variables or function calls, only literal "
            "arithmetic."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "Arithmetic expression using only digits, "
                        "+ - * / ( ) and spaces. Example: '42 * 17 + 3'."
                    ),
                }
            },
            "required": ["expression"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "lookup_inventory",
        "description": (
            "Look up the on-hand count, warehouse location, and price for a "
            "Summitline Outfitters SKU. Use this whenever the user asks "
            "about stock levels or availability of a specific SKU."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sku": {
                    "type": "string",
                    "description": (
                        "Summitline product SKU, e.g. 'SMT-HIKE-TENT-02'."
                    ),
                }
            },
            "required": ["sku"],
            "additionalProperties": False,
        },
    },
]


# Name -> callable. `_run_tools` in main.py looks up functions here.
DISPATCH: Dict[str, Callable[..., Any]] = {
    "get_weather": get_weather,
    "calculate": calculate,
    "lookup_inventory": lookup_inventory,
}


__all__ = ["TOOL_SCHEMAS", "DISPATCH", "get_weather", "calculate", "lookup_inventory"]
