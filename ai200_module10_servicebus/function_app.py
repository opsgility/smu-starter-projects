"""Azure Functions v4 Python (V2 programming model) — three triggers.

Triggers:
  - HTTP POST /api/classify        — synchronous classifier
  - Service Bus queue 'shipments'  — async background processor with DLQ
  - Cosmos change feed on 'incidents' — emits derived events to an out queue

The student completes three TODOs in Steps 4, 5, and 6.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# ---- Shared rules (re-used from prior modules) -------------------------------

RULES = [
    (("water", "soaked", "wet", "rain", "flood"), "water-damage"),
    (("crushed", "crush", "smashed", "broken", "dent"), "crush-damage"),
    (("missing", "lost", "stolen", "not found"), "missing-item"),
    (("late", "delayed", "delay", "stuck"), "delayed"),
    (("frozen", "thawed", "warm", "spoiled", "temperature"), "temperature-excursion"),
]


def classify_text(description: str) -> str:
    t = description.lower()
    for keys, label in RULES:
        if any(k in t for k in keys):
            return label
    return "unknown"


# ---- 1. HTTP trigger --------------------------------------------------------

@app.route(route="classify", methods=["POST"])
def classify(req: func.HttpRequest) -> func.HttpResponse:
    """Synchronous classification endpoint.

    TODO(step4): replace this body. Read JSON {"shipment_id":..., "description":...}
    from req.get_json(), call classify_text(description), return func.HttpResponse
    with a JSON body containing shipment_id and label, status_code=200.
    """
    raise NotImplementedError("Step 4: implement classify HTTP trigger")


# ---- 2. Service Bus queue trigger -------------------------------------------

@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="shipments",
    connection="ServiceBusConnection",
)
def process_shipment(msg: func.ServiceBusMessage) -> None:
    """Process a queued shipment payload.

    TODO(step5): replace this body. Parse msg.get_body() as JSON, call
    classify_text on its description, and logging.info() a structured line.
    Raise on missing 'description' to exercise the platform's DLQ.
    """
    raise NotImplementedError("Step 5: implement process_shipment SB trigger")


# ---- 3. Cosmos DB change feed trigger + output queue binding ----------------

@app.cosmos_db_trigger(
    arg_name="incidents",
    container_name="incidents",
    database_name="northwind",
    connection="CosmosDbConnection",
    lease_container_name="leases",
    create_lease_container_if_not_exists=True,
)
@app.service_bus_queue_output(
    arg_name="outQueue",
    queue_name="classifications",
    connection="ServiceBusConnection",
)
def on_incident_changes(
    incidents: func.DocumentList,
    outQueue: func.Out[str],
) -> None:
    """Convert raw incidents into classification events on the out queue.

    TODO(step6): replace this body. For each document in `incidents`:
      1. payload = json.loads(doc.to_json())
      2. label = classify_text(payload.get("text",""))
      3. emit = {"shipment_id": payload.get("id"), "tenant": payload.get("tenantId"), "label": label}
    Then outQueue.set(json.dumps(list_of_emits)).
    """
    raise NotImplementedError("Step 6: implement on_incident_changes cosmos trigger")
