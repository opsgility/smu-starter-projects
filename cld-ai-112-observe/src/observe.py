"""Structured Claude client wrapper — emits one JSON log line per call."""

import hashlib, json, sys, time, uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
import anthropic

load_dotenv()

PRICES = {
    "claude-haiku-4-5": (0.80, 4.00),
    "claude-sonnet-5":  (3.00, 15.00),
    "claude-opus-5-5":  (15.00, 75.00),
}


def emit(record):
    print(json.dumps(record))


class ObservedClient:
    def __init__(self):
        self._c = anthropic.Anthropic()

    def messages_create(self, **kw):
        trace_id = str(uuid.uuid4())[:8]
        user_text = ""
        for m in kw.get("messages", []):
            if isinstance(m.get("content"), str):
                user_text += m["content"]
        input_hash = hashlib.sha256(user_text.encode()).hexdigest()[:12]
        t0 = time.perf_counter()
        r = self._c.messages.create(**kw)
        elapsed_ms = int((time.perf_counter() - t0) * 1000)

        p_in, p_out = PRICES.get(kw.get("model", ""), (3.0, 15.0))
        cache_read = getattr(r.usage, "cache_read_input_tokens", 0)
        cache_write = getattr(r.usage, "cache_creation_input_tokens", 0)
        cost = (r.usage.input_tokens * p_in + cache_write * (p_in * 0.25) +
                cache_read * (p_in * 0.1) + r.usage.output_tokens * p_out) / 1e6

        text = next((b.text for b in r.content if b.type == "text"), "")
        refused = any(s in text.lower() for s in ("i can only", "i cannot", "i can't"))

        emit({
            "ts": datetime.now(timezone.utc).isoformat(),
            "trace_id": trace_id,
            "model": kw.get("model"),
            "latency_ms": elapsed_ms,
            "input_tokens": r.usage.input_tokens,
            "output_tokens": r.usage.output_tokens,
            "cache_read": cache_read,
            "cache_write": cache_write,
            "cost_usd": round(cost, 6),
            "cache_hit": cache_read > 0,
            "refused": refused,
            "stop_reason": r.stop_reason,
            "input_hash": input_hash,
        })
        return r, trace_id


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "What's the Sev-1 SLA?"
    c = ObservedClient()
    r, tid = c.messages_create(
        model="claude-sonnet-5", max_tokens=300,
        system="You are the Orion support assistant.",
        messages=[{"role": "user", "content": q}])
    text = next((b.text for b in r.content if b.type == "text"), "")
    print(f"\n[trace_id={tid}] {text}", file=sys.stderr)
