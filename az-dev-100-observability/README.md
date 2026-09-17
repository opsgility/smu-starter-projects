# az-dev-100-observability

Anchorline Outdoors storefront — starter for the observability module.

## Endpoints

- `GET /health` — instant 200
- `GET /version` — build tag
- `GET /fast` — ~40ms simulated fast path
- `GET /slow` — ~1200ms simulated slow path (deliberate)
- `GET /checkout` — multi-span operation (inventory → payment → persist), ~700ms typical, 5% throw rate
- `GET /fail` — always 500 (for alert testing)

## Instrumentation

The starter has `Azure.Monitor.OpenTelemetry.AspNetCore` referenced but the wiring line commented out. Exercise 1 has you enable it.

The `Anchorline.Storefront` Meter emits a custom counter (`anchorline.checkout.requests`) and histogram (`anchorline.checkout.duration_ms`). The `Anchorline.Storefront` ActivitySource emits nested spans on `/checkout` (inventory-lookup, payment-authorize, order-persist).

## Load generator

`scripts/load.sh https://<host> 120 5` — 120 seconds at ~5 rps mixing /fast /slow /checkout /fail. Used to populate KQL queries.
