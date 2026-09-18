# az-dev-300-data-layer

TaskForge data layer starter: EF Core 9 migrations for SQL tenant metadata + RLS policies + Cosmos with hierarchical partition key + a runner that seeds and verifies isolation.

## Env
- `SQL_SERVER` (e.g. `tf-sql-<suffix>.database.windows.net`)
- `SQL_DB` (default `TaskForge`)
- `COSMOS_ENDPOINT`

## Steps
1. Apply `sql/rls.sql` to your Azure SQL DB via `sqlcmd` (with an Entra admin login).
2. Create the Cosmos container: `az cosmosdb sql container create --account-name ... --database-name TaskForge --name tasks --partition-key-path "/tenantId,/projectId" --partition-key-version 2`
3. `dotnet run` — verifies RLS filter + writes a Cosmos doc.
