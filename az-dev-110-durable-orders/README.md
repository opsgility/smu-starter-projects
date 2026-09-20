# az-dev-110-durable-orders

Anchorline's Durable Functions order-approval workflow.

## Endpoints

- `POST /api/orders` — start orchestration; returns `instanceId`.
- `GET /api/orders/{instanceId}` — status.
- `POST /api/orders/{instanceId}/approve` — send `ApprovalReceived` external event (body contains `true` or `false`).

## Workflow

1. Validate stock (activity).
2. Charge card (activity).
3. If `Total > 10000`: wait up to 3 days for `ApprovalReceived` (external event with timeout).
4. Fan-out: warehouse, shipping, email in parallel.
