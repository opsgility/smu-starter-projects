"""Ridgevault Financial market-data + compliance MCP server.

Exposes two tools via fastmcp:
  - get_market_snapshot(tickers)        -> price/volume/change per ticker
  - check_position_limit(issuer, sector, notional_usd) -> allowed vs blocked verdict

The same server code runs BOTH locally (Exercise 2/3) and inside the Azure Function
(Exercise 4). The Function App imports `build_asgi_app` from function_wrapper.py,
which reuses the `mcp` object defined here.

Local run:
  python src/mcp_server/ridgevault_tools.py
  # binds http://127.0.0.1:8123/mcp
"""
from __future__ import annotations
import json
from pathlib import Path

from fastmcp import FastMCP


DATA_DIR = Path(__file__).resolve().parents[2] / "data"

with (DATA_DIR / "market-snapshot-sample.json").open() as fh:
    _snapshots = json.load(fh)
SNAPSHOTS_BY_TICKER: dict[str, dict] = {row["ticker"]: row for row in _snapshots}

with (DATA_DIR / "position-limits.json").open() as fh:
    _limits = json.load(fh)
ISSUER_LIMITS: dict[str, float] = {row["issuer"]: row["limit_usd"] for row in _limits["issuers"]}
SECTOR_LIMITS: dict[str, float] = {row["sector"]: row["limit_usd"] for row in _limits["sectors"]}


mcp = FastMCP("ridgevault-tools")


@mcp.tool()
def get_market_snapshot(tickers: list[str]) -> dict:
    """Return the latest end-of-day market snapshot for a list of Ridgevault-covered tickers.

    Args:
        tickers: A list of ticker symbols, e.g. ["AAPL", "MSFT", "JPM"].

    Returns:
        A dict keyed by ticker. Each value has:
          - last_close (float, USD)
          - day_change_pct (float)
          - avg_volume_30d (int)
          - sector (str)
          - as_of (str, ISO date)
        Missing tickers are returned under the "not_covered" key so the agent can
        distinguish "no data" from "bad request".
    """
    results: dict[str, dict] = {}
    missing: list[str] = []
    for ticker in tickers:
        row = SNAPSHOTS_BY_TICKER.get(ticker.upper())
        if row is None:
            missing.append(ticker)
        else:
            results[ticker.upper()] = row
    return {"snapshots": results, "not_covered": missing}


@mcp.tool()
def check_position_limit(issuer: str, sector: str, notional_usd: float) -> dict:
    """Return whether a proposed position size is inside Ridgevault's per-issuer AND per-sector limits.

    Args:
        issuer: The issuer/company name, e.g. "Apple Inc.".
        sector: The GICS sector, e.g. "Information Technology".
        notional_usd: The proposed position size in USD.

    Returns:
        {
          "allowed": bool,
          "issuer_limit_usd": float,
          "sector_limit_usd": float,
          "reason": str  # human-readable explanation
        }
    A position is allowed only when notional_usd <= both the issuer limit AND
    the sector limit. Unknown issuers / sectors return allowed=False.
    """
    issuer_limit = ISSUER_LIMITS.get(issuer)
    sector_limit = SECTOR_LIMITS.get(sector)

    if issuer_limit is None:
        return {
            "allowed": False,
            "issuer_limit_usd": 0.0,
            "sector_limit_usd": sector_limit or 0.0,
            "reason": f"Issuer {issuer!r} is not on Ridgevault's covered list — trade blocked pending analyst review.",
        }
    if sector_limit is None:
        return {
            "allowed": False,
            "issuer_limit_usd": issuer_limit,
            "sector_limit_usd": 0.0,
            "reason": f"Sector {sector!r} is not defined in Ridgevault's limit table — trade blocked pending policy update.",
        }

    if notional_usd > issuer_limit:
        return {
            "allowed": False,
            "issuer_limit_usd": issuer_limit,
            "sector_limit_usd": sector_limit,
            "reason": f"Notional ${notional_usd:,.0f} exceeds the ${issuer_limit:,.0f} per-issuer limit for {issuer}.",
        }
    if notional_usd > sector_limit:
        return {
            "allowed": False,
            "issuer_limit_usd": issuer_limit,
            "sector_limit_usd": sector_limit,
            "reason": f"Notional ${notional_usd:,.0f} exceeds the ${sector_limit:,.0f} per-sector limit for {sector}.",
        }

    return {
        "allowed": True,
        "issuer_limit_usd": issuer_limit,
        "sector_limit_usd": sector_limit,
        "reason": f"Notional ${notional_usd:,.0f} is inside both the ${issuer_limit:,.0f} issuer limit and the ${sector_limit:,.0f} sector limit.",
    }


if __name__ == "__main__":
    # Local run — bind to 127.0.0.1:8123.
    mcp.run(transport="http", host="127.0.0.1", port=8123)
