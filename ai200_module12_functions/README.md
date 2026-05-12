# ai200_module12_functions — Azure Functions (HTTP + Service Bus + Cosmos triggers)

Starter project for **AI-200 Module 12**. A single Python V2 function app
with three triggers. The student fills in three TODOs.

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `function_app.py` | TODOs in Steps 4 (HTTP), 5 (Service Bus), 6 (Cosmos change feed) |
| `host.json` | Functions host config (extension bundle 4.x) |
| `local.settings.json.example` | Copy to `local.settings.json` and fill in connection settings |
| `requirements.txt` | `azure-functions` only — bindings come from extension bundle |
| `scripts/enqueue_shipments.py` | Pushes test messages onto the `shipments` queue |
| `scripts/insert_incident.py` | Inserts an incident to fire the change feed |
| `.funcignore` | Pre-set so `func azure functionapp publish` doesn't ship junk |
