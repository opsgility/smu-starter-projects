"""Compare Haiku vs Sonnet vs Opus on the same image."""

import base64, json, time, sys
from dotenv import load_dotenv
import anthropic

load_dotenv()

img_path = sys.argv[1] if len(sys.argv) > 1 else "receipt.png"
with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

media = "image/png" if img_path.endswith(".png") else "image/jpeg"

MODELS = [
    ("claude-haiku-4-5", 0.80, 4.00),      # per M in/out $
    ("claude-sonnet-5",  3.00, 15.00),
    ("claude-opus-5-5",  15.00, 75.00),
]

PROMPT = "Extract this receipt to JSON: {merchant, total}. Reply with ONLY the JSON."

client = anthropic.Anthropic()
for model, p_in, p_out in MODELS:
    t0 = time.perf_counter()
    r = client.messages.create(model=model, max_tokens=256,
        messages=[{"role":"user","content":[
            {"type":"image","source":{"type":"base64","media_type":media,"data":img_b64}},
            {"type":"text","text":PROMPT}]}])
    ms = int((time.perf_counter() - t0) * 1000)
    text = next((b.text for b in r.content if b.type == "text"), "").strip("`json \n")
    cost = r.usage.input_tokens * p_in / 1e6 + r.usage.output_tokens * p_out / 1e6
    print(f"\n=== {model} ({ms}ms, ${cost:.5f}) ===")
    print(text)
