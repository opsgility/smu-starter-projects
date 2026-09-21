# az-dev-110-webhook-fanout

Anchorline's order webhook — one HTTP POST fans out to three destinations:

- **Cosmos DB** (`Anchorline.Orders`) — the order document (partition key `/id`)
- **Blob Storage** (`order-payloads/orders/{orderId}.json`) — payload archive
- **Service Bus** (`order-notifications` queue) — downstream notification

Two functions:

| Function | Route | Purpose |
| --- | --- | --- |
| `PlaceOrder` | `POST /api/webhooks/orders` | Accept an order payload; fan out to Cosmos + Blob + Service Bus |
| `GetOrder`   | `GET  /api/webhooks/orders/{orderId}` | Read back the archived order from Cosmos |

All three downstream writes use **`DefaultAzureCredential`** — the ARM template
grants the Function App's system-assigned managed identity the required roles
(Storage Blob Data Owner, Cosmos SQL Data Contributor, Azure Service Bus Data Owner).
No connection strings, no keys.

## App settings

The Function App reads these settings (all provisioned by ARM template 118):

- `AzureWebJobsStorage__accountName`
- `COSMOS_ENDPOINT`, `COSMOS_DATABASE`, `COSMOS_CONTAINER`
- `SERVICEBUS_FULLYQUALIFIEDNAMESPACE`, `SERVICEBUS_QUEUE`

## Payload shape

```json
{
  "orderId": "ord-100",
  "customerId": "c-42",
  "items": [ { "sku": "KAYAK", "qty": 1 } ]
}
```
