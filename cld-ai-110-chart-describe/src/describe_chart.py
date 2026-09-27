"""First Claude vision call — describe a chart."""

import base64, os, sys
from dotenv import load_dotenv
import anthropic

load_dotenv()

img_path = sys.argv[1] if len(sys.argv) > 1 else "chart.png"
with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

media_type = "image/png" if img_path.endswith(".png") else "image/jpeg"

client = anthropic.Anthropic()
r = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64",
                                          "media_type": media_type,
                                          "data": img_b64}},
            {"type": "text", "text": "Describe this chart in 3 sentences. What's the main trend?"}
        ]
    }]
)

text = next((b.text for b in r.content if b.type == "text"), "")
print(text)
print(f"\n[tokens: {r.usage.input_tokens} in / {r.usage.output_tokens} out]")
