# az-dev-140-capstone

Anchorline global multi-tenant Cosmos SaaS backend.

## Config

- `Anchorline:CosmosEndpoint`
- `Anchorline:MiClientId`

## Endpoints

- `POST /api/orders` — place an order (hierarchical partition key)
- `GET  /api/orders?tenantId=X` — tenant-scoped
- `GET  /api/orders?tenantId=X&customerId=Y` — customer-scoped (single logical partition)
- `POST /api/products` — upsert a product with a vector embedding
- `POST /api/recommend` — vector search for similar products

## Design

- **orders** container: hierarchical partition key `/tenantId/customerId`, TTL enabled per-doc.
- **summary** container: `/tenantId` partition (change feed projector would fill).
- **products** container: `/category` partition + integrated vector index on `/embedding`.
