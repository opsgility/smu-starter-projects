# az-dev-130-capstone

Anchorline multi-tenant SaaS data layer — shared DB, RLS, MI auth.

## Config

- `Anchorline:SqlServer` — SQL server FQDN.
- `Anchorline:SqlDatabase` — `AnchorlineSaaS`.
- `Anchorline:MiClientId` — User-Assigned MI client id (from ARM output).

## Endpoints

- `GET  /whoami` — DB user + session TenantId.
- `POST /customers` — insert a Customer for the header's tenant.
- `GET  /customers` — list Customers visible to the header's tenant (RLS scopes).
- `GET  /leak-attempt` — SELECT COUNT(*) with NO WHERE clause; proves RLS still scopes.

All endpoints require `X-Tenant-Id: <int>` header. The middleware reads it, and the connection sets `SESSION_CONTEXT('TenantId')`.

## Verify RLS

```
# Insert data for two tenants
curl -X POST -H "X-Tenant-Id: 1" -H content-type:application/json -d '{"name":"Alice","email":"a@ex.com"}' https://<app>/customers
curl -X POST -H "X-Tenant-Id: 2" -H content-type:application/json -d '{"name":"Bob","email":"b@ex.com"}' https://<app>/customers

# Read as tenant 1 — sees only Alice
curl -H "X-Tenant-Id: 1" https://<app>/customers

# Bulk-count as tenant 1 — sees only 1 row despite "SELECT COUNT(*) FROM Customer" with no WHERE
curl -H "X-Tenant-Id: 1" https://<app>/leak-attempt
```
