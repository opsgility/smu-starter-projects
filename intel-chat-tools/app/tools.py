"""Tool definitions for the Sentinel Intelligence Bureau OSINT Concierge.

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

All data in this module is non-classified, fictional, and synthesized for
training. The Sentinel Intelligence Bureau (SIB) is a notional open-source
intelligence organization used for the AI-3016 course.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List


# ---------------------------------------------------------------------------
# Python implementations of the three tools
# ---------------------------------------------------------------------------

# A very small mock open-source news feed. In a real OSINT Concierge this
# would hit a public RSS aggregator or news API.
_NEWS: Dict[str, Dict[str, Any]] = {
    "balkan-elections": {
        "headline": "Balkan regional elections monitored by OSCE observers",
        "source": "Public Wire Service",
        "date": "2026-05-28",
        "summary": (
            "Independent observers report orderly polling in three Balkan "
            "states; turnout up 4% over the prior cycle."
        ),
    },
    "sahel-security": {
        "headline": "Sahel security cooperation talks resume in Niamey",
        "source": "Open Diplomacy Brief",
        "date": "2026-05-30",
        "summary": (
            "Regional ministers re-open coordination on counter-trafficking "
            "and humanitarian corridors after a six-month pause."
        ),
    },
    "indo-pacific-tensions": {
        "headline": "Indo-Pacific maritime cooperation exercise concludes",
        "source": "Open Pacific Monitor",
        "date": "2026-06-01",
        "summary": (
            "A multilateral exercise emphasizing freedom of navigation and "
            "humanitarian assistance wrapped up off the coast of Mindanao."
        ),
    },
    "arctic-shipping": {
        "headline": "Northern Sea Route opens earlier than seasonal average",
        "source": "Polar Logistics Digest",
        "date": "2026-05-25",
        "summary": (
            "Commercial shippers report ice-free transit windows widening "
            "10 days ahead of the 10-year average."
        ),
    },
    "andean-supply-chain": {
        "headline": "Andean copper export volumes hit 12-month high",
        "source": "Open Commodity Tracker",
        "date": "2026-05-22",
        "summary": (
            "Three Andean producers report export volumes 14% above the "
            "trailing 12-month average amid stable spot prices."
        ),
    },
    "horn-of-africa-aid": {
        "headline": "Horn of Africa aid corridor reopens through Djibouti",
        "source": "Humanitarian Wire",
        "date": "2026-05-18",
        "summary": (
            "Three NGOs resume convoy operations after a two-week pause for "
            "route assessment; UN observers confirm safe passage."
        ),
    },
}

# A mock public threat-feed indicator database. The indicator
# `OSINT-IND-2024-1042` is the one referenced in the exercises and
# test_client.py. All entries describe non-classified, fictional patterns
# used for training only.
_THREAT_FEED: Dict[str, Dict[str, Any]] = {
    "OSINT-IND-2024-1042": {
        "name": "Disinformation campaign targeting Balkan elections",
        "category": "Influence Operation",
        "confidence": "Moderate",
        "first_observed": "2024-09-12",
        "last_observed": "2026-05-28",
        "tags": ["balkan-elections", "social-media", "synthetic-media"],
        "summary": (
            "Coordinated inauthentic behavior across three social platforms "
            "amplifying false claims about polling-station closures."
        ),
    },
    "OSINT-IND-2024-1107": {
        "name": "Public phishing kit targeting humanitarian NGOs",
        "category": "Cybercrime",
        "confidence": "High",
        "first_observed": "2024-11-03",
        "last_observed": "2026-05-30",
        "tags": ["phishing", "ngo", "credential-theft"],
        "summary": (
            "Open-source phishing kit reused in spear-phishing emails "
            "impersonating UN procurement officers."
        ),
    },
    "OSINT-IND-2024-1183": {
        "name": "Maritime spoofing pattern in Indo-Pacific lanes",
        "category": "Geospatial Anomaly",
        "confidence": "Low",
        "first_observed": "2024-12-19",
        "last_observed": "2026-06-01",
        "tags": ["ais-spoofing", "indo-pacific", "maritime"],
        "summary": (
            "Public AIS data shows recurring GPS-spoofing artifacts near "
            "three Indo-Pacific shipping lanes during night hours."
        ),
    },
}


def get_open_source_news(topic: str) -> Dict[str, Any]:
    """Return the latest open-source news item for a topic key (mock data)."""
    record = _NEWS.get(topic.strip().lower())
    if record is None:
        return {"topic": topic, "error": "unknown topic"}
    return {
        "topic": topic,
        "headline": record["headline"],
        "source": record["source"],
        "date": record["date"],
        "summary": record["summary"],
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


def lookup_threat_feed(indicator_id: str) -> Dict[str, Any]:
    """Return the public threat-feed entry for an OSINT indicator id."""
    record = _THREAT_FEED.get(indicator_id.strip().upper())
    if record is None:
        return {"indicator_id": indicator_id, "error": "indicator not found"}
    return {
        "indicator_id": indicator_id.strip().upper(),
        "name": record["name"],
        "category": record["category"],
        "confidence": record["confidence"],
        "first_observed": record["first_observed"],
        "last_observed": record["last_observed"],
        "tags": record["tags"],
        "summary": record["summary"],
    }


# ---------------------------------------------------------------------------
# Responses-API tool schemas (FLAT shape — no inner `function:` wrapper)
# ---------------------------------------------------------------------------

TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "name": "get_open_source_news",
        "description": (
            "Fetch the latest open-source news item for an OSINT topic. Use "
            "this whenever an analyst asks about recent public reporting on "
            "a regional or thematic topic (e.g. 'balkan-elections', "
            "'sahel-security', 'indo-pacific-tensions')."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": (
                        "OSINT topic slug, lowercase with hyphens, e.g. "
                        "'balkan-elections' or 'arctic-shipping'."
                    ),
                }
            },
            "required": ["topic"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "calculate",
        "description": (
            "Evaluate a simple arithmetic expression (addition, subtraction, "
            "multiplication, division, parentheses). Use this for any math "
            "an analyst asks about — rate calculations, percentage changes, "
            "time-delta totals, headcount ratios, etc. Do NOT pass variables "
            "or function calls, only literal arithmetic."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "Arithmetic expression using only digits, "
                        "+ - * / ( ) and spaces. Example: '4200 / 28000 * 100'."
                    ),
                }
            },
            "required": ["expression"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "lookup_threat_feed",
        "description": (
            "Look up the public threat-feed entry for a Sentinel Intelligence "
            "Bureau OSINT indicator id. Use this whenever an analyst asks "
            "about a specific indicator id like 'OSINT-IND-2024-1042'."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "indicator_id": {
                    "type": "string",
                    "description": (
                        "SIB OSINT indicator id, e.g. 'OSINT-IND-2024-1042'."
                    ),
                }
            },
            "required": ["indicator_id"],
            "additionalProperties": False,
        },
    },
]


# Name -> callable. `_run_tools` in main.py looks up functions here.
DISPATCH: Dict[str, Callable[..., Any]] = {
    "get_open_source_news": get_open_source_news,
    "calculate": calculate,
    "lookup_threat_feed": lookup_threat_feed,
}


__all__ = [
    "TOOL_SCHEMAS",
    "DISPATCH",
    "get_open_source_news",
    "calculate",
    "lookup_threat_feed",
]
