# az-dev-150-capstone

Anchorline capstone: OrderApi + OrderProcessor with MI + KEDA + OTel.

## Services

- **OrderApi** — external HTTPS. POST /orders → Cosmos + Service Bus. Uses MI.
- **OrderProcessor** — Service Bus consumer, KEDA-scaled 0-10 replicas, uses MI for SB.

## Env vars (both services)

- `MI_CLIENT_ID` — user-assigned MI client id
- `SB_NAMESPACE` — Service Bus FQDN
- `SB_QUEUE` — `orders`
- `APPLICATIONINSIGHTS_CONNECTION_STRING` — App Insights
- `APP_VERSION` — v1 or v2 (for blue/green demo on OrderApi)
- `COSMOS_ENDPOINT` — for OrderApi only
