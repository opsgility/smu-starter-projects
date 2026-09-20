# az-dev-100-managed-identity

Anchorline Outdoors storefront wired to Azure Storage, Key Vault, Azure SQL, and Cosmos DB using **managed identity** — no connection strings, no shared keys.

## Endpoints

- `GET /health` — liveness
- `GET /version` — reports the build tag from `AZ_DEV_100_BUILD_TAG`
- `GET /whoami` — decodes the app's own identity token payload (audience, tenant, objectId)
- `GET /blobs` — lists the first 20 blob names in `Anchorline:BlobContainer` using `BlobServiceClient` + `DefaultAzureCredential`
- `GET /secret/{name}` — reads a Key Vault secret by name; returns a masked value
- `GET /products` — reads `SELECT TOP 10 * FROM dbo.Products` from Azure SQL using `SqlConnection.AccessToken`
- `GET /catalog` — reads `SELECT TOP 10 * FROM c` from Cosmos DB using `CosmosClient` + `DefaultAzureCredential`

## Configuration

App settings on the Web App (or environment variables locally):

- `Anchorline:StorageAccountUrl` — e.g. `https://anchorlineimg.blob.core.windows.net`
- `Anchorline:BlobContainer` — default `products`
- `Anchorline:KeyVaultUrl` — e.g. `https://anchorline-kv.vault.azure.net`
- `Anchorline:SqlServer` — e.g. `anchorline-sql.database.windows.net`
- `Anchorline:SqlDatabase` — default `anchorline-products`
- `Anchorline:CosmosEndpoint` — e.g. `https://anchorline-cosmos.documents.azure.com:443/`
- `Anchorline:CosmosDatabase` — default `Anchorline`
- `Anchorline:CosmosContainer` — default `Catalog`

## RBAC required

- **Storage**: `Storage Blob Data Contributor` scoped to the storage account
- **Key Vault**: `Key Vault Secrets User` scoped to the vault (vault must have `enableRbacAuthorization: true`)
- **Azure SQL**: SQL-native user — `CREATE USER [<app-name>] FROM EXTERNAL PROVIDER;` then `ALTER ROLE db_datareader ADD MEMBER [<app-name>];`
- **Cosmos DB**: `Cosmos DB Built-in Data Contributor` (`00000000-0000-0000-0000-000000000002`) — assigned via `az cosmosdb sql role assignment create`, NOT the portal IAM blade

## Run locally

```bash
az login
dotnet run
curl http://localhost:5000/whoami
```

`DefaultAzureCredential` will pick up your `az login` credentials locally and switch to the App Service system-assigned identity in Azure.
