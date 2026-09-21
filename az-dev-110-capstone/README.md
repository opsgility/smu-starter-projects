# az-dev-110-capstone

Anchorline capstone — order intake pipeline as three Functions with OpenTelemetry instrumentation.

## Flow

1. `POST /api/orders` → `StartOrder` (HTTP intake) starts an orchestration.
2. `OrderPipelineOrchestrator` runs `ValidateActivity` then `WriteToCosmosActivity`.
3. `WriteToCosmosActivity` writes the record to `Anchorline.Orders` via the Cosmos SDK
   using `DefaultAzureCredential` (RBAC-only — `COSMOS_ENDPOINT` app setting, no key).

## Order shape

`POST /api/orders` body:

```json
{ "orderId": "cap-001", "customerId": "c-42", "sku": "AO-TENT-2P", "quantity": 1, "total": 249.50 }
```

`ValidateActivity` accepts orders with `quantity > 0 && total > 0`.

## Custom metrics

- `anchorline.capstone.orders_received` (counter)
- `anchorline.capstone.validation_ms` (histogram)
- `anchorline.capstone.cosmos_writes` (counter)

`ActivitySource` `Anchorline.Capstone` emits nested spans `validate-order` and `cosmos-write`.

## App settings (provisioned by ARM)

- `COSMOS_ENDPOINT` — Cosmos account document endpoint (RBAC-only, `disableLocalAuth=true`)
- `COSMOS_DATABASE` — `Anchorline`
- `COSMOS_CONTAINER` — `Orders`
- `INPUTS_CONTAINER` — `order-inputs` blob container
- `AzureWebJobsStorage__accountName` — storage account name (identity-based)
- `APPLICATIONINSIGHTS_CONNECTION_STRING` + `APPLICATIONINSIGHTS_AUTHENTICATION_STRING=Authorization=AAD`

## Load test

`scripts/load.sh <base-url> <function-key> 500 20` sends 500 orders in batches of 20.
