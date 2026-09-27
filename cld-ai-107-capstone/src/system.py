"""Multi-agent Orion capstone with structured logging + traces."""

import json, os, sys, time, uuid
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import anthropic


TRACES: list[dict] = []


def log_event(trace_id: str, agent: str, event: str, **kwargs):
    TRACES.append({"trace_id": trace_id, "agent": agent, "event": event, "ts": time.time(), **kwargs})


ROUTE_SCHEMA = {
    "name": "route",
    "input_schema": {"type": "object",
                     "properties": {"specialist": {"type": "string", "enum": ["quick", "complex", "high_stakes"]}},
                     "required": ["specialist"]},
}


def route(client, model, request: str, trace_id: str) -> str:
    log_event(trace_id, "router", "start", request=request[:100])
    resp = client.messages.create(model=model, max_tokens=100,
        system="Classify the request: quick (single lookup), complex (needs decomposition), high_stakes (needs debate).",
        tools=[ROUTE_SCHEMA], tool_choice={"type":"tool","name":"route"},
        messages=[{"role":"user","content": request}])
    specialist = next(b.input for b in resp.content if b.type == "tool_use")["specialist"]
    log_event(trace_id, "router", "end", specialist=specialist)
    return specialist


def quick_specialist(client, model, request: str, trace_id: str) -> str:
    log_event(trace_id, "quick", "start")
    resp = client.messages.create(model=model, max_tokens=300,
        system="Answer briefly and directly.",
        messages=[{"role":"user","content": request}])
    text = next((b.text for b in resp.content if b.type == "text"), "")
    log_event(trace_id, "quick", "end", output_len=len(text))
    return text


def complex_specialist(client, model, request: str, trace_id: str) -> str:
    """TODO: decompose into 2 sub-questions, answer each, synthesize.
    Log each sub-step with log_event using trace_id.
    HINT: use route-like tool_use schema, then parallel workers, then synthesize."""
    # Simplified: just answer with a longer system prompt
    log_event(trace_id, "complex", "start")
    resp = client.messages.create(model=model, max_tokens=800,
        system="You are a research assistant. Break the question mentally into components, address each, then synthesize a 5-sentence answer.",
        messages=[{"role":"user","content": request}])
    text = next((b.text for b in resp.content if b.type == "text"), "")
    log_event(trace_id, "complex", "end", output_len=len(text))
    return text


def high_stakes_specialist(client, model, request: str, trace_id: str) -> str:
    log_event(trace_id, "high_stakes", "start")
    perspectives = ["cautious", "growth-focused", "user-first"]

    def one(perspective):
        r = client.messages.create(model=model, max_tokens=250,
            system=f"You are a {perspective} advisor.",
            messages=[{"role":"user","content": request}])
        return (perspective, next((b.text for b in r.content if b.type == "text"), ""))

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(one, perspectives))
    for p, _ in results:
        log_event(trace_id, "high_stakes", "advisor_done", perspective=p)

    formatted = "\n\n".join(f"[{p}]:\n{a}" for p, a in results)
    resp = client.messages.create(model=model, max_tokens=500,
        messages=[{"role":"user","content": f"Question: {request}\n\n{formatted}\n\nSynthesize."}])
    text = next((b.text for b in resp.content if b.type == "text"), "")
    log_event(trace_id, "high_stakes", "end", output_len=len(text))
    return text


def handle(client, model, request: str) -> str:
    trace_id = str(uuid.uuid4())[:8]
    specialist = route(client, model, request, trace_id)
    if specialist == "quick":
        return quick_specialist(client, model, request, trace_id)
    if specialist == "complex":
        return complex_specialist(client, model, request, trace_id)
    if specialist == "high_stakes":
        return high_stakes_specialist(client, model, request, trace_id)
    return "(unknown routing)"


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    reqs = [
        "What is the current SLA for Sev-1?",  # quick
        "Should we scale our support team horizontally or invest in more automation?",  # complex
        "Should we launch the new pricing tier this quarter or wait?",  # high_stakes
    ]
    for r in reqs:
        print(f"\n{'='*70}\nREQUEST: {r}")
        print(f"ANSWER: {handle(client, model, r)[:400]}...")

    print(f"\n\n=== TRACE SUMMARY ({len(TRACES)} events) ===")
    from collections import defaultdict
    by_trace = defaultdict(list)
    for t in TRACES:
        by_trace[t["trace_id"]].append(t)
    for tid, events in by_trace.items():
        print(f"\nTrace {tid}:")
        for e in events:
            extras = {k:v for k,v in e.items() if k not in ("trace_id","ts")}
            print(f"  {extras}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
