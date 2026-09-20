# az-dev-110-webhook-fanout

Anchorline's order webhook — one HTTP POST triggers three simultaneous writes via bindings:

- CosmosDB (`Anchorline.Orders`) — the order record
- Blob Storage (`order-payloads/{id}.json`) — the raw payload archive
- Service Bus queue (`order-notifications`) — downstream notification

Zero SDK code — everything is attribute-driven.
