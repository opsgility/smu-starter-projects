# ai200_module11_eventgrid — Event Grid Filters, Custom Events & Retries

Starter project for **AI-200 Module 11**. You create a custom Event Grid
topic, deploy the FastAPI subscriber as a Container App, wire a
subscription with a SQL filter and a Service Bus DLQ, then publish events
and confirm only matching ones reach the subscriber.

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `lib/eg_publisher.py` | `publish_event` TODO (Step 5) |
| `app/subscriber.py` | FastAPI `POST /events` TODO (Step 7) handles validation + events |
| `scripts/publish_demo.py` | Publishes 20 events of mixed labels |
| `Dockerfile` | Builds the subscriber image for ACA |
