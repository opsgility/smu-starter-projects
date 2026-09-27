"""Orion assistant shell — config + health + first call."""

import os, sys
from dotenv import load_dotenv
import anthropic

load_dotenv()


class Config:
    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.model = os.environ.get("ORION_MODEL", "claude-sonnet-5")
        self.max_daily = float(os.environ.get("ORION_MAX_DAILY_USD", "10.00"))
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY missing — set it in .env")


def healthz(cfg):
    checks = {
        "api_key_present": bool(cfg.api_key),
        "model_set": bool(cfg.model),
        "budget_configured": cfg.max_daily > 0,
    }
    ok = all(checks.values())
    return {"ok": ok, "checks": checks, "model": cfg.model, "budget_usd": cfg.max_daily}


def ask(cfg, question):
    client = anthropic.Anthropic(api_key=cfg.api_key)
    r = client.messages.create(model=cfg.model, max_tokens=400,
        system="You are the Orion support assistant. Be concise.",
        messages=[{"role": "user", "content": question}])
    return next((b.text for b in r.content if b.type == "text"), "")


def main():
    cfg = Config()
    if len(sys.argv) > 1 and sys.argv[1] == "healthz":
        import json
        print(json.dumps(healthz(cfg), indent=2))
        return
    q = " ".join(sys.argv[1:]) or "What are your operating principles?"
    print(ask(cfg, q))


if __name__ == "__main__":
    main()
