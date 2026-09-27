"""Canary rollout with metric gate."""

import hashlib, json, statistics, time
from collections import defaultdict
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

BASELINE = {"prompt_version": "v1", "system": "You are Orion support. Be helpful."}
CANARY = {"prompt_version": "v2",
          "system": "You are Orion support. If you cannot answer with certainty, refuse politely."}
CANARY_PCT = 5  # % of traffic to canary


def config_for(user_id):
    return CANARY if (hash(user_id) % 100) < CANARY_PCT else BASELINE


def ask(user_id, question):
    cfg = config_for(user_id)
    t0 = time.perf_counter()
    r = client.messages.create(model="claude-sonnet-5", max_tokens=200,
        system=cfg["system"],
        messages=[{"role": "user", "content": question}])
    ms = int((time.perf_counter() - t0) * 1000)
    text = next((b.text for b in r.content if b.type == "text"), "")
    refused = any(s in text.lower() for s in ("cannot", "can't help", "not able", "let me route"))
    return {"prompt_version": cfg["prompt_version"], "latency_ms": ms,
            "refused": refused, "text_len": len(text)}


def simulate():
    metrics = defaultdict(list)
    questions = ["Sev-1 SLA?", "auth method?", "export CSV?", "refund policy?",
                 "SSO available?", "trial length?", "backup schedule?"] * 8

    for i, q in enumerate(questions):
        user_id = f"user-{i}"
        m = ask(user_id, q)
        metrics[m["prompt_version"]].append(m)

    print(json.dumps({"canary_pct": CANARY_PCT}))
    for v, records in metrics.items():
        p95 = sorted(r["latency_ms"] for r in records)[int(len(records) * 0.95)]
        ref_rate = sum(1 for r in records if r["refused"]) / len(records)
        print(json.dumps({
            "prompt_version": v,
            "requests": len(records),
            "p95_ms": p95,
            "refusal_rate": round(ref_rate, 3),
        }))


if __name__ == "__main__":
    simulate()
