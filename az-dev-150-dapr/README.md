# az-dev-150-dapr

Two-service Dapr demo:

- **OrderApi** — publishes `OrderCreated` via Dapr pub/sub
- **OrderProcessor** — subscribes via `[Topic("eventbus", "OrderCreated")]` and persists state via Dapr state store

## Components

- `components/eventbus.yaml`   — Dapr pub/sub, backed by Service Bus
- `components/statestore.yaml` — Dapr state store, backed by Cosmos DB

Both components register at the ACA environment level via `az containerapp env dapr-component set`.
