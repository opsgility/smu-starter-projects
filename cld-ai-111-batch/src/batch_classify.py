"""Batch-classify 20 Orion support tickets at 50% cost."""

import time
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

TICKETS = [
    "Login page loads then blank screen",
    "How do I export my Q3 report?",
    "Billing charged twice for August",
    "Feature request: bulk import CSV",
    "API 500 on /v2/reports/generate",
    "Password reset email not received",
    "Dashboard slow after latest update",
    "Trial expired, want to convert",
    "Data missing from Aug 12 backup",
    "SSO login broken since morning",
    "Add graph type: waterfall chart",
    "OAuth callback failing intermittently",
    "Where's the docs for the CLI?",
    "Refund for cancelled subscription",
    "Report shows wrong currency symbol",
    "Alert threshold not saving",
    "Can I invite external users?",
    "429 Too Many Requests all day",
    "Wrong timezone in exported data",
    "Delete account request",
]

requests = [
    {"custom_id": f"tkt-{i}",
     "params": {"model": "claude-haiku-4-5", "max_tokens": 50,
                "messages": [{"role": "user", "content":
                              f"Classify this ticket as ONE of: bug, billing, feature, howto. Ticket: {t}\nReply with just the label."}]}}
    for i, t in enumerate(TICKETS)
]

batch = client.messages.batches.create(requests=requests)
print(f"batch id: {batch.id}")
print(f"status: {batch.processing_status}")
print(f"submitted {len(requests)} requests")

while True:
    b = client.messages.batches.retrieve(batch.id)
    print(f"  polling... {b.processing_status} (counts: {b.request_counts})")
    if b.processing_status == "ended":
        break
    time.sleep(15)

print(f"\n=== results ===")
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        text = next((b.text for b in result.result.message.content if b.type == "text"), "").strip()
        idx = int(result.custom_id.split("-")[1])
        print(f"  {result.custom_id}: {text:<10} — {TICKETS[idx][:50]}")
    else:
        print(f"  {result.custom_id}: FAILED ({result.result.type})")
