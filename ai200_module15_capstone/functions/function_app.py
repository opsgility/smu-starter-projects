"""Capstone Azure Function — consumes northwind-events queue and writes
audit records to Cosmos. Pre-written; the student only deploys it."""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone

import azure.functions as func
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

app = func.FunctionApp()


def _audit_container():
    endpoint = os.environ["COSMOS_ENDPOINT"]
    key = os.environ.get("COSMOS_KEY")
    client = CosmosClient(endpoint, credential=key) if key else CosmosClient(endpoint, credential=DefaultAzureCredential())
    db = client.get_database_client("northwind")
    return db.get_container_client("audit")


@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="northwind-events",
    connection="ServiceBusConnection",
)
def on_event(msg: func.ServiceBusMessage) -> None:
    body = json.loads(msg.get_body().decode("utf-8"))
    body["received_at"] = datetime.now(timezone.utc).isoformat()
    body["id"] = f"audit-{msg.message_id}"
    body["tenantId"] = body.get("tenant", "unknown")
    _audit_container().upsert_item(body)
    logging.info("audit_written id=%s event=%s", body["id"], body.get("event"))
