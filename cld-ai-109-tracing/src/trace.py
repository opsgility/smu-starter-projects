"""Structured tracing wrapper for Claude calls."""

import json, os, sys, time, uuid
from dotenv import load_dotenv
import anthropic


SONNET_IN = 3.00 / 1e6; SONNET_OUT = 15.00 / 1e6


def emit(record: dict):
    print(json.dumps(record))


def traced_call(client, model, trace_id, agent_name, **create_kwargs):
    t0 = time.perf_counter()
    try:
        resp = client.messages.create(model=model, **create_kwargs)
        latency_ms = int((time.perf_counter() - t0) * 1000)
        in_tok = resp.usage.input_tokens
        out_tok = resp.usage.output_tokens
        cost = in_tok * SONNET_IN + out_tok * SONNET_OUT
        emit({"trace_id": trace_id, "agent": agent_name, "status": "ok",
              "input_tokens": in_tok, "output_tokens": out_tok, "cost_usd": round(cost, 6),
              "latency_ms": latency_ms, "stop_reason": resp.stop_reason})
        return resp
    except Exception as e:
        emit({"trace_id": trace_id, "agent": agent_name, "status": "error",
              "error_type": type(e).__name__, "error": str(e)[:100]})
        raise


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    trace_id = str(uuid.uuid4())[:8]

    # Simulate a 3-call request
    traced_call(client, model, trace_id, "classifier", max_tokens=100,
                messages=[{"role":"user","content":"Category of: dashboard down 40min"}])
    traced_call(client, model, trace_id, "responder", max_tokens=200,
                messages=[{"role":"user","content":"Draft a support reply."}])
    traced_call(client, model, trace_id, "summarizer", max_tokens=100,
                messages=[{"role":"user","content":"Summarize this convo in one sentence."}])


if __name__ == "__main__":
    main()
