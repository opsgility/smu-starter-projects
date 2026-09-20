# az-dev-110-capstone

Anchorline capstone — order intake pipeline as three Functions with OpenTelemetry instrumentation.

## Flow

1. `POST /api/orders` → `IntakeOrder` (HTTP intake) starts an orchestration.
2. `OrderPipelineOrchestrator` runs `ValidateActivity` then `WriteToCosmosActivity`.
3. `WriteToCosmosActivity` has `[CosmosDBOutput]` — record lands in `Anchorline.Orders`.

## Custom metrics

- `anchorline.capstone.orders_received` (counter)
- `anchorline.capstone.validation_ms` (histogram)
- `anchorline.capstone.cosmos_writes` (counter)

`ActivitySource` `Anchorline.Capstone` emits nested spans `validate-order` and `cosmos-write`.

## Load test

`scripts/load.sh <base-url> <key> 500 10` sends 500 orders at ~10 rps.
