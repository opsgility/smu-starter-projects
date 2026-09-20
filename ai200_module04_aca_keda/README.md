# ai200_module04_aca_keda — Azure Container Apps + KEDA scaling

Starter project for **AI-200 Module 4**. You will deploy two apps into a single
Container Apps environment:

1. `classifier` — the FastAPI service with an HTTP scaler
2. `classifier-worker` — a Python consumer with an `azure-servicebus` scaler that scales 0→N off queue depth

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `app/main.py` | FastAPI service with `/healthz`, `/classify`, `/process` (the slow endpoint that drives HTTP scaling) |
| `Dockerfile` | Builds the FastAPI service |
| `worker/worker.py` | Service Bus queue consumer using `DefaultAzureCredential` |
| `worker/Dockerfile` | Builds the worker image |
| `worker/requirements.txt` | Worker deps |
| `scripts/loadgen.py` | Async load generator that hits `/process` |
| `scripts/enqueue.py` | Pushes N test messages onto the queue to drive worker scale-out |
| `scripts/requirements.txt` | Deps for the local scripts |

## What you will build

- One Container Apps environment (`cae-ai200`) with Log Analytics wired in
- The `classifier` app with HTTP scaler (1→10 replicas, target 20 concurrent requests)
- A Service Bus namespace + queue (`shipments-in`)
- The `classifier-worker` app with `azure-servicebus` scaler (0→10 replicas)
- A loadgen + enqueue run that proves both scalers work
