"""L2 tool-arg guardrail: validates arguments the model wants to pass to a tool.

You wire this in exercise 3. It is a `FunctionMiddleware` that runs BEFORE every tool
call and short-circuits if the arguments fail Ridgevault business rules:

  - `portfolio_lookup(account_number, as_of_date)`
      * account_number must match ^RV-[0-9]{8}$ (Ridgevault account-number regex)
      * as_of_date must be within the last 7 years (Ridgevault SOX retention window)

  - `client_record(account_number)`
      * account_number must match ^RV-[0-9]{8}$

If the arguments fail, the middleware sets `context.result` to a structured error and
returns WITHOUT awaiting `call_next()` — the tool never runs, the model sees the error
in the tool result, and the flow continues (BLOCK verdict = short-circuit; the tool
is not called; no side effects).
"""
from __future__ import annotations
import re
from datetime import date, timedelta

from agent_framework import FunctionInvocationContext, FunctionMiddleware  # type: ignore

RIDGEVAULT_ACCOUNT_RE = re.compile(r"^RV-[0-9]{8}$")
MAX_LOOKBACK_YEARS = 7


class ToolArgValidator(FunctionMiddleware):
    """Enforces Ridgevault argument shape on `portfolio_lookup` + `client_record`."""

    async def process(self, context: FunctionInvocationContext, call_next):  # noqa: D401
        fname = context.function.name
        args = context.arguments or {}

        if fname in ("portfolio_lookup", "client_record"):
            acct = str(args.get("account_number", ""))
            # TODO exercise 3 step 2: if acct does not match RIDGEVAULT_ACCOUNT_RE,
            # set context.result = { "error": "GUARDRAIL_BLOCKED",
            #                        "layer": "L2",
            #                        "reason": f"account_number must match ^RV-[0-9]{{8}}$, got {acct!r}" }
            # and RETURN without calling call_next().
            pass

        if fname == "portfolio_lookup":
            as_of_raw = args.get("as_of_date")
            # TODO exercise 3 step 3: parse as_of_raw as an ISO date. If it is older than
            # MAX_LOOKBACK_YEARS from today, or in the future, set context.result with
            # layer=L2, reason='as_of_date outside 7-year retention window' and RETURN.
            _ = as_of_raw
            _ = date, timedelta  # keep imports referenced for the student's implementation
            pass

        await call_next()  # arguments are OK — tool runs
