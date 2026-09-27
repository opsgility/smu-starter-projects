"""Smoke test — inspect the inferred schemas + invoke each tool."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from server import mcp


def dump_schemas():
    if hasattr(mcp, "_tool_manager") and hasattr(mcp._tool_manager, "_tools"):
        for name, tool in mcp._tool_manager._tools.items():
            print(f"\n=== {name} ===")
            if hasattr(tool, "parameters"):
                print(json.dumps(tool.parameters, indent=2))
            elif hasattr(tool, "input_schema"):
                print(json.dumps(tool.input_schema, indent=2))
    else:
        print("(SDK layout doesn't expose tool manager directly.)")


def main():
    dump_schemas()
    print("\nDirect invocations:")
    try:
        from server import set_priority, process_refund, register_sla_rule, RefundRequest, SLARule
        print(f"  set_priority: {set_priority('T-1', 'high')}")
        print(f"  process_refund: {process_refund(RefundRequest(customer_id='acme', amount_usd=100, reason='outage credit'))}")
        print(f"  register_sla_rule (valid): {register_sla_rule(SLARule(severity=1, response_min=10))}")
        try:
            register_sla_rule(SLARule(severity=1, response_min=30))
        except Exception as e:
            print(f"  register_sla_rule (invalid Sev-1 with 30min) rejected: {e}")
    except (ImportError, Exception) as e:
        print(f"  Import/call failed (TODOs unfilled?): {e}")


if __name__ == "__main__":
    main()
