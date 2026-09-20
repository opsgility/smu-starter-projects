"""FastAPI Event Grid subscriber.

Handles:
  - Validation handshake (Microsoft.EventGrid.SubscriptionValidationEvent)
  - Custom events (Northwind.Shipment.Classified, etc.)

Step 7 has TODOs for the student to fill in.
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("subscriber")

app = FastAPI(title="Northwind EG Subscriber", version="1.0.0")


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/events")
async def events(request: Request) -> Any:
    """Event Grid will POST a JSON array of envelopes here.

    TODO(step7): replace this body. For each event in the JSON array:
      1. If event.get("eventType") == "Microsoft.EventGrid.SubscriptionValidationEvent":
         return {"validationResponse": event["data"]["validationCode"]}
      2. Else log it and add to a counter.
    Return a 200-OK list of {"status":"accepted"} entries.

    Reference: https://learn.microsoft.com/azure/event-grid/receive-events
    """
    raise NotImplementedError("Step 7: implement events handler")
